#!/usr/bin/env node

/**
 * OpenWork Auto-Submission Bot
 * 
 * Fetches open jobs from the OpenWork API, filters by configurable criteria,
 * generates submissions from templates, and submits while respecting rate limits.
 */

import { readFileSync, appendFileSync, existsSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Logger ──────────────────────────────────────────────────────────────────

class Logger {
  constructor(config) {
    this.level = config?.level || 'info';
    this.file = config?.file ? join(__dirname, config.file) : null;
    this.levels = { debug: 0, info: 1, warn: 2, error: 3 };
  }

  _log(level, message, data) {
    if (this.levels[level] < this.levels[this.level]) return;
    const ts = new Date().toISOString();
    const entry = `[${ts}] [${level.toUpperCase()}] ${message}${data ? ' ' + JSON.stringify(data) : ''}`;
    console.log(entry);
    if (this.file) {
      try { appendFileSync(this.file, entry + '\n'); } catch {}
    }
  }

  debug(msg, data) { this._log('debug', msg, data); }
  info(msg, data) { this._log('info', msg, data); }
  warn(msg, data) { this._log('warn', msg, data); }
  error(msg, data) { this._log('error', msg, data); }
}

// ── Rate Limiter ────────────────────────────────────────────────────────────

class RateLimiter {
  constructor(maxPerHour = 10) {
    this.maxPerHour = maxPerHour;
    this.timestamps = [];
  }

  canProceed() {
    const oneHourAgo = Date.now() - 3600000;
    this.timestamps = this.timestamps.filter(t => t > oneHourAgo);
    return this.timestamps.length < this.maxPerHour;
  }

  record() {
    this.timestamps.push(Date.now());
  }

  waitTimeMs() {
    if (this.canProceed()) return 0;
    const oneHourAgo = Date.now() - 3600000;
    this.timestamps = this.timestamps.filter(t => t > oneHourAgo);
    return this.timestamps[0] - oneHourAgo + 100;
  }
}

// ── API Client ──────────────────────────────────────────────────────────────

class OpenWorkClient {
  constructor(baseUrl, apiKey, logger, retryPolicy) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.logger = logger;
    this.maxRetries = retryPolicy?.maxRetries || 3;
    this.backoffMs = retryPolicy?.backoffMs || 1000;
  }

  async _fetch(path, options = {}) {
    const url = `${this.baseUrl}${path}`;
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      ...options.headers,
    };

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        this.logger.debug(`Request: ${options.method || 'GET'} ${url} (attempt ${attempt + 1})`);
        const res = await fetch(url, { ...options, headers });

        if (res.status === 429) {
          const retryAfter = parseInt(res.headers.get('retry-after') || '60', 10);
          this.logger.warn(`Rate limited. Waiting ${retryAfter}s`);
          await sleep(retryAfter * 1000);
          continue;
        }

        if (!res.ok) {
          const body = await res.text().catch(() => '');
          throw new Error(`HTTP ${res.status}: ${body}`);
        }

        return await res.json();
      } catch (err) {
        if (attempt === this.maxRetries) throw err;
        const wait = this.backoffMs * Math.pow(2, attempt);
        this.logger.warn(`Retry in ${wait}ms: ${err.message}`);
        await sleep(wait);
      }
    }
  }

  async fetchJobs() {
    return this._fetch('/jobs');
  }

  async submitJob(jobId, submission) {
    return this._fetch(`/jobs/${jobId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ submission }),
    });
  }
}

// ── Template Engine ─────────────────────────────────────────────────────────

function renderTemplate(template, vars) {
  return template.replace(/\{(\w+)\}/g, (_, key) => vars[key] ?? `{${key}}`);
}

function generateSubmission(job, templates) {
  const templateKey = job.tags?.some(t => ['node', 'python', 'rust', 'solidity', 'code'].includes(t?.toLowerCase()))
    ? 'technical' : 'default';
  const template = templates[templateKey] || templates.default;

  const vars = {
    solution: `Solution for: ${job.title || job.id}`,
    features: (job.tags || []).map(t => `- ${t}`).join('\n') || '- General purpose solution',
    approach: `Addressing the requirements outlined in "${job.title || 'this job'}"`,
    testing: '- Unit tests included\n- Manual verification completed',
    documentation: '- README with setup instructions\n- Inline code comments',
  };

  return renderTemplate(template, vars);
}

// ── Filters ─────────────────────────────────────────────────────────────────

function matchesFilters(job, filters) {
  if (filters.minReward && (job.reward || 0) < filters.minReward) return false;

  if (filters.tags?.length) {
    const jobTags = (job.tags || []).map(t => t?.toLowerCase());
    if (!filters.tags.some(t => jobTags.includes(t.toLowerCase()))) return false;
  }

  if (filters.excludeTags?.length) {
    const jobTags = (job.tags || []).map(t => t?.toLowerCase());
    if (filters.excludeTags.some(t => jobTags.includes(t.toLowerCase()))) return false;
  }

  return true;
}

// ── Helpers ─────────────────────────────────────────────────────────────────

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function loadConfig() {
  const configPath = join(__dirname, 'config.json');
  if (!existsSync(configPath)) {
    throw new Error('config.json not found. Copy config.json and fill in your API key.');
  }
  const config = JSON.parse(readFileSync(configPath, 'utf-8'));
  if (!config.apiKey) {
    throw new Error('apiKey is required in config.json');
  }
  return config;
}

// ── State Persistence ───────────────────────────────────────────────────────

const STATE_FILE = join(__dirname, '.state.json');

function loadState() {
  try { return JSON.parse(readFileSync(STATE_FILE, 'utf-8')); }
  catch { return { submittedJobs: [] }; }
}

function saveState(state) {
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const dryRun = process.argv.includes('--dry-run');
  const config = loadConfig();
  const logger = new Logger(config.logging);
  const client = new OpenWorkClient(config.apiBaseUrl, config.apiKey, logger, config.retryPolicy);
  const rateLimiter = new RateLimiter(config.filters?.maxSubmissionsPerHour || 10);
  const state = loadState();

  logger.info(`Bot started${dryRun ? ' (DRY RUN)' : ''}`);

  // Fetch jobs
  let jobsResponse;
  try {
    jobsResponse = await client.fetchJobs();
  } catch (err) {
    logger.error('Failed to fetch jobs', { error: err.message });
    process.exit(1);
  }

  const jobs = Array.isArray(jobsResponse) ? jobsResponse : (jobsResponse?.jobs || jobsResponse?.data || []);
  logger.info(`Fetched ${jobs.length} jobs`);

  // Filter
  const filtered = jobs.filter(j => matchesFilters(j, config.filters || {}));
  logger.info(`${filtered.length} jobs match filters`);

  // Remove already-submitted
  const pending = filtered.filter(j => !state.submittedJobs.includes(j.id));
  logger.info(`${pending.length} new jobs to submit`);

  let submitted = 0;
  for (const job of pending) {
    if (!rateLimiter.canProceed()) {
      const waitMs = rateLimiter.waitTimeMs();
      logger.info(`Rate limit reached. Waiting ${Math.ceil(waitMs / 1000)}s`);
      await sleep(waitMs);
    }

    const submission = generateSubmission(job, config.templates || {});
    logger.info(`Submitting to job ${job.id}: ${job.title || 'Untitled'}`, { reward: job.reward });

    if (!dryRun) {
      try {
        const result = await client.submitJob(job.id, submission);
        rateLimiter.record();
        state.submittedJobs.push(job.id);
        saveState(state);
        submitted++;
        logger.info(`Submitted successfully`, { jobId: job.id, result });
      } catch (err) {
        logger.error(`Submission failed for ${job.id}`, { error: err.message });
      }
    } else {
      logger.info(`[DRY RUN] Would submit to ${job.id}`);
      submitted++;
    }
  }

  logger.info(`Done. Submitted: ${submitted}/${pending.length}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
