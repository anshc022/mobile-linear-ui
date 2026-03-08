const WEBHOOK_URL = "https://discord.com/api/webhooks/1478134362565251155/qDqhoVtRrQFJ2WJdTT39qPUWSLexbHVLccKyvp7kbJuX-KpnnU2Pm-b5zsy3OrCRdvIZ";

const statusEl = () => document.getElementById("status");
const logEl = () => document.getElementById("logEntries");

function setStatus(msg, type = "") {
  const el = statusEl();
  el.textContent = msg;
  el.className = "status " + type;
}

function addLog(msg, ok = true) {
  const el = logEl();
  const time = new Date().toLocaleTimeString();
  const cls = ok ? "ok" : "fail";
  const entry = document.createElement("div");
  entry.className = "log-entry";
  entry.innerHTML = `<span class="time">${time}</span> — <span class="${cls}">${msg}</span>`;
  
  // Remove "no activity" placeholder
  if (el.children.length === 1 && el.children[0].textContent.includes("No activity")) {
    el.innerHTML = "";
  }
  el.insertBefore(entry, el.firstChild);
}

async function sendToDiscord(content, label) {
  if (!content || content.trim().length < 10) {
    setStatus("❌ No content found on page", "error");
    addLog("No content found", false);
    return;
  }

  setStatus("⏳ Sending to Echo...", "loading");

  const chunks = [];
  const maxLen = 1900;
  let remaining = `**${label}**\n\n${content}`;
  
  while (remaining.length > 0) {
    if (remaining.length <= maxLen) {
      chunks.push(remaining);
      break;
    }
    let breakAt = remaining.lastIndexOf('\n', maxLen);
    if (breakAt < maxLen * 0.5) breakAt = maxLen;
    chunks.push(remaining.substring(0, breakAt));
    remaining = remaining.substring(breakAt);
  }

  try {
    for (let i = 0; i < chunks.length; i++) {
      const resp = await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "Echo Reader", content: chunks[i] })
      });
      if (!resp.ok && resp.status !== 204) throw new Error(`HTTP ${resp.status}`);
      if (i < chunks.length - 1) await new Promise(r => setTimeout(r, 500));
    }
    
    setStatus(`✅ Sent! (${chunks.length} part${chunks.length > 1 ? 's' : ''})`, "success");
    addLog(`${label} — ${chunks.length} part(s)`, true);
  } catch (err) {
    setStatus(`❌ Failed: ${err.message}`, "error");
    addLog(`Failed: ${err.message}`, false);
  }
}

// Send full page
document.getElementById("sendFull").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => ({ title: document.title, url: window.location.href, text: document.body.innerText })
  });
  const { title, url, text } = results[0].result;
  await sendToDiscord(`**URL:** ${url}\n\n${text}`, `📄 ${title}`);
});

// Send selected text
document.getElementById("sendSelected").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => ({ title: document.title, url: window.location.href, selected: window.getSelection().toString() })
  });
  const { title, url, selected } = results[0].result;
  if (!selected || selected.trim().length < 5) {
    setStatus("❌ No text selected — highlight text first", "error");
    addLog("No text selected", false);
    return;
  }
  await sendToDiscord(`**URL:** ${url}\n\n${selected}`, `✂️ Selection from: ${title}`);
});

// Extract quiz
document.getElementById("sendQuiz").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const body = document.body.innerText;
      const lines = body.split('\n');
      const qLines = [];
      let capture = false;
      for (const line of lines) {
        const t = line.trim();
        if (/^(Q\d|Question\s*\d|\d+[\.\)]\s|What |Which |How |Why |When |Where |Select |Choose |Match |True |False |Check |Refer )/i.test(t)) capture = true;
        if (/^[A-D][\.\)]\s|^[○●□■☐☑]/.test(t)) capture = true;
        if (capture) { qLines.push(t); if (t === '') capture = false; }
      }
      const text = qLines.length > 5 ? qLines.join('\n') : body;
      return { title: document.title, url: window.location.href, text, extracted: qLines.length > 5 };
    }
  });
  const { title, url, text, extracted } = results[0].result;
  const label = extracted ? `🎯 Quiz: ${title}` : `📄 Full Page (no quiz found): ${title}`;
  await sendToDiscord(`**URL:** ${url}\n\n${text}`, label);
});

// Screenshot
document.getElementById("sendScreenshot").addEventListener("click", async () => {
  setStatus("📸 Capturing...", "loading");
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const dataUrl = await chrome.tabs.captureVisibleTab(null, { format: "png" });
    const resp = await fetch(dataUrl);
    const blob = await resp.blob();
    
    const formData = new FormData();
    formData.append("payload_json", JSON.stringify({
      username: "Echo Reader",
      content: `**📸 Screenshot:** ${tab.title}\n**URL:** ${tab.url}`
    }));
    formData.append("files[0]", blob, "screenshot.png");
    
    const hookResp = await fetch(WEBHOOK_URL, { method: "POST", body: formData });
    if (!hookResp.ok && hookResp.status !== 204) throw new Error(`HTTP ${hookResp.status}`);
    
    setStatus("✅ Screenshot sent!", "success");
    addLog("📸 Screenshot sent", true);
  } catch (err) {
    setStatus(`❌ Failed: ${err.message}`, "error");
    addLog(`Screenshot failed: ${err.message}`, false);
  }
});
