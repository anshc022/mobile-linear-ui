const WEBHOOK_URL = "https://discord.com/api/webhooks/1478134362565251155/qDqhoVtRrQFJ2WJdTT39qPUWSLexbHVLccKyvp7kbJuX-KpnnU2Pm-b5zsy3OrCRdvIZ";

const statusEl = () => document.getElementById("status");

function setStatus(msg, type = "") {
  const el = statusEl();
  el.textContent = msg;
  el.className = "status " + type;
}

async function sendToDiscord(content, label) {
  if (!content || content.trim().length < 10) {
    setStatus("❌ No content found on page", "error");
    return;
  }

  setStatus("⏳ Sending to Echo...", "loading");

  // Discord max message length is 2000, split into chunks
  const chunks = [];
  const maxLen = 1900;
  
  // First chunk gets the label header
  let remaining = `**📄 ${label}**\n\n${content}`;
  
  while (remaining.length > 0) {
    if (remaining.length <= maxLen) {
      chunks.push(remaining);
      break;
    }
    // Find a good break point
    let breakAt = remaining.lastIndexOf('\n', maxLen);
    if (breakAt < maxLen * 0.5) breakAt = maxLen;
    chunks.push(remaining.substring(0, breakAt));
    remaining = remaining.substring(breakAt);
  }

  try {
    for (let i = 0; i < chunks.length; i++) {
      const body = {
        username: "Echo Reader",
        content: chunks[i]
      };
      
      const resp = await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      
      if (!resp.ok && resp.status !== 204) {
        throw new Error(`HTTP ${resp.status}`);
      }
      
      // Rate limit: wait between chunks
      if (i < chunks.length - 1) {
        await new Promise(r => setTimeout(r, 500));
      }
    }
    
    setStatus(`✅ Sent! (${chunks.length} part${chunks.length > 1 ? 's' : ''})`, "success");
  } catch (err) {
    setStatus(`❌ Failed: ${err.message}`, "error");
  }
}

// Send full page text
document.getElementById("sendFull").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return {
        title: document.title,
        url: window.location.href,
        text: document.body.innerText
      };
    }
  });
  
  const { title, url, text } = results[0].result;
  await sendToDiscord(
    `**URL:** ${url}\n\n${text}`,
    title || "Full Page"
  );
});

// Send selected text only
document.getElementById("sendSelected").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return {
        title: document.title,
        url: window.location.href,
        selected: window.getSelection().toString()
      };
    }
  });
  
  const { title, url, selected } = results[0].result;
  if (!selected || selected.trim().length < 5) {
    setStatus("❌ No text selected — highlight text first", "error");
    return;
  }
  await sendToDiscord(
    `**URL:** ${url}\n\n${selected}`,
    `Selection from: ${title}`
  );
});

// Extract quiz/questions
document.getElementById("sendQuiz").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  const results = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const body = document.body.innerText;
      const url = window.location.href;
      const title = document.title;
      
      // Try to extract question patterns
      const lines = body.split('\n');
      const questionLines = [];
      let capture = false;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        // Match question patterns
        if (/^(Q\d|Question\s*\d|\d+[\.\)]\s|What |Which |How |Why |When |Where |Select |Choose |Match |True |False |Check |Refer )/i.test(line)) {
          capture = true;
        }
        // Also capture radio/checkbox options
        if (/^[A-D][\.\)]\s|^○|^●|^□|^■|^☐|^☑/.test(line)) {
          capture = true;
        }
        if (capture) {
          questionLines.push(line);
          if (line === '') {
            capture = false;
          }
        }
      }
      
      // If pattern matching found stuff, use it; otherwise send full page
      const extracted = questionLines.length > 5 
        ? questionLines.join('\n') 
        : body;
      
      return { title, url, text: extracted, wasExtracted: questionLines.length > 5 };
    }
  });
  
  const { title, url, text, wasExtracted } = results[0].result;
  const label = wasExtracted 
    ? `🎯 Quiz Extracted: ${title}` 
    : `📄 Full Page (no quiz pattern found): ${title}`;
  
  await sendToDiscord(`**URL:** ${url}\n\n${text}`, label);
});

// Send screenshot
document.getElementById("sendScreenshot").addEventListener("click", async () => {
  setStatus("📸 Capturing screenshot...", "loading");
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const dataUrl = await chrome.tabs.captureVisibleTab(null, { format: "png" });
    
    // Convert data URL to blob
    const resp = await fetch(dataUrl);
    const blob = await resp.blob();
    
    // Send via webhook as file
    const formData = new FormData();
    formData.append("payload_json", JSON.stringify({
      username: "Echo Reader",
      content: `**📸 Screenshot:** ${tab.title}\n**URL:** ${tab.url}`
    }));
    formData.append("files[0]", blob, "screenshot.png");
    
    const hookResp = await fetch(WEBHOOK_URL, {
      method: "POST",
      body: formData
    });
    
    if (!hookResp.ok && hookResp.status !== 204) {
      throw new Error(`HTTP ${hookResp.status}`);
    }
    
    setStatus("✅ Screenshot sent!", "success");
  } catch (err) {
    setStatus(`❌ Failed: ${err.message}`, "error");
  }
});
