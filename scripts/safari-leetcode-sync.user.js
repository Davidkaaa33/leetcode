// ==UserScript==
// @name         LeetCode -> Davidkaaa33/leetcode (Safari)
// @namespace    https://github.com/Davidkaaa33/leetcode
// @version      1.0.0
// @description  Sync accepted Python submissions through Safari, without GitHub LeetCode session cookies.
// @match        https://leetcode.com/problems/*
// @run-at       document-idle
// @noframes
// @grant        GM.getValue
// @grant        GM.setValue
// @grant        GM.xmlHttpRequest
// @connect      api.github.com
// @inject-into  content
// ==/UserScript==

(async function () {
  "use strict";
  const OWNER = "Davidkaaa33";
  const REPO = "leetcode";
  const TOKEN_KEY = "githubFineGrainedToken";
  const slugMatch = location.pathname.match(/^\/problems\/([a-z0-9-]+)\/?/);
  if (!slugMatch || !globalThis.GM || !GM.getValue || !GM.xmlHttpRequest) return;
  const slug = slugMatch[1];
  let busy = false;
  let pending = 0;
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

  // This element lives only in the Safari page; it never contains the token.
  const panel = document.createElement("div");
  panel.style.cssText = "position:fixed;bottom:16px;right:16px;z-index:2147483646;background:#161b22;color:#e6edf3;border:1px solid #59636e;border-radius:6px;padding:8px;font:12px system-ui,sans-serif;max-width:300px";
  const setting = document.createElement("button");
  const sync = document.createElement("button");
  const note = document.createElement("div");
  const buttonStyle = "background:#30363d;color:#e6edf3;border:1px solid #59636e;border-radius:4px;padding:5px 8px;margin-right:6px;cursor:pointer";
  setting.style.cssText = buttonStyle;
  sync.style.cssText = buttonStyle;
  setting.textContent = "GitHub token";
  sync.textContent = "Sync Accepted";
  note.textContent = "LeetCode Safari sync";
  note.style.marginTop = "6px";
  panel.append(setting, sync, note);
  const mount = () => { if (!panel.isConnected && document.body) document.body.append(panel); };
  mount();
  function report(message) { note.textContent = message; console.info("[LeetCode Safari Sync]", message); }

  setting.addEventListener("click", async () => {
    const token = prompt("Paste a fine-grained GitHub token (Contents: read/write, only Davidkaaa33/leetcode). It stays in local Userscripts storage. Leave blank to cancel:");
    if (!token) return;
    const value = token.trim();
    if (!/^github_pat_[A-Za-z0-9_]+$/.test(value)) {
      report("Expected a fine-grained token starting with github_pat_");
      return;
    }
    await GM.setValue(TOKEN_KEY, value);
    report("Token saved locally. Use Sync Accepted for a test.");
  });

  async function graphql(query, variables) {
    const csrf = document.cookie.split("; ").find(part => part.startsWith("csrftoken="));
    const headers = { "Content-Type": "application/json", "Accept": "application/json" };
    if (csrf) headers["x-csrftoken"] = decodeURIComponent(csrf.slice(10));
    const response = await fetch("https://leetcode.com/graphql/", {
      method: "POST", credentials: "include", headers,
      body: JSON.stringify({ query, variables })
    });
    if (!response.ok) throw new Error("LeetCode API HTTP " + response.status + " — ensure you are signed in");
    const result = await response.json();
    if (result.errors?.length) throw new Error("LeetCode GraphQL: " + result.errors[0].message);
    return result.data;
  }

  async function newestAccepted() {
    const variants = [
      "query($s:String!){questionSubmissionList(offset:0,limit:15,questionSlug:$s){submissions{id statusDisplay lang timestamp}}}",
      "query($s:String!){submissionList(offset:0,limit:15,questionSlug:$s){submissions{id statusDisplay lang timestamp}}}"
    ];
    let lastError;
    for (const query of variants) {
      try {
        const data = await graphql(query, { s: slug });
        const records = data.questionSubmissionList?.submissions || data.submissionList?.submissions;
        if (Array.isArray(records)) return records.find(item => item.statusDisplay === "Accepted") || null;
      } catch (e) { lastError = e; }
    }
    throw lastError || new Error("No submission-list API available");
  }

  async function codeFor(id) {
    const data = await graphql(
      "query($id:Int!){submissionDetails(submissionId:$id){code statusDisplay lang{name} question{title titleSlug difficulty}}}",
      { id: Number(id) }
    );
    if (!data.submissionDetails?.code) throw new Error("Accepted code not available yet");
    return data.submissionDetails;
  }

  function encodeBase64(text) {
    const bytes = new TextEncoder().encode(text);
    let raw = "";
    for (const byte of bytes) raw += String.fromCharCode(byte);
    return btoa(raw);
  }

  async function github(path, token, method, payload) {
    const response = await GM.xmlHttpRequest({
      method, url: "https://api.github.com/repos/" + OWNER + "/" + REPO + "/contents/" + path,
      headers: {
        Authorization: "Bearer " + token,
        Accept: "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28"
      },
      data: payload ? JSON.stringify(payload) : undefined,
      responseType: "text",
      timeout: 20000
    });
    let body = {};
    try { body = JSON.parse(response.responseText || "{}"); } catch (_) {}
    if (response.status !== 200 && response.status !== 201 && !(method === "GET" && response.status === 404)) {
      throw new Error("GitHub API " + response.status + ": " + (body.message || "request failed"));
    }
    return body;
  }

  async function syncLatest({ after = 0 } = {}) {
    if (busy) return false;
    busy = true;
    try {
      const token = await GM.getValue(TOKEN_KEY, "");
      if (!token) throw new Error("First click GitHub token to configure access");
      const latest = await newestAccepted();
      if (!latest) throw new Error("No accepted submission found for this problem");
      // Do not upload an older accepted solution after a new failed submission.
      if (after && Number(latest.timestamp) < after) return false;
      if (String(await GM.getValue("synced:" + slug, "")) === String(latest.id)) {
        if (!after) report("Already synced this submission");
        return true;
      }
      const language = String(latest.lang || "").toLowerCase();
      if (!["python", "python3", "python2"].includes(language)) {
        throw new Error("Currently supports Python solutions only (" + language + ")");
      }
      report("Reading accepted solution…");
      const details = await codeFor(latest.id);
      if (details.statusDisplay && details.statusDisplay !== "Accepted") throw new Error("Submission was not accepted");
      const difficulty = String(details.question?.difficulty || "").toLowerCase();
      if (!["easy", "medium", "hard"].includes(difficulty)) throw new Error("Could not identify difficulty");
      const path = "problems/" + difficulty + "/" + slug.replace(/-/g, "_") + "/solution.py";
      // Store the actual accepted code, not the current Monaco editor text.
      const code = details.code.replace(/\r\n/g, "\n");
      const existing = await github(path, token, "GET");
      const payload = {
        message: "Solve " + (details.question?.title || slug) + " on LeetCode",
        content: encodeBase64(code.endsWith("\n") ? code : code + "\n"),
        branch: "main"
      };
      if (existing.sha) payload.sha = existing.sha;
      report("Pushing to GitHub…");
      const result = await github(path, token, "PUT", payload);
      if (!result.commit?.sha) throw new Error("GitHub did not confirm a commit");
      await GM.setValue("synced:" + slug, String(latest.id));
      report("Synced: " + (details.question?.title || slug));
      return true;
    } catch (err) {
      report("Sync failed: " + (err?.message || err));
      return false;
    } finally { busy = false; }
  }

  sync.addEventListener("click", () => syncLatest());

  // Detect an explicit Submit action. Poll the authenticated submission API,
  // not the Monaco editor or an unstable Accepted DOM selector.
  document.addEventListener("click", event => {
    const button = event.target?.closest?.("button");
    if (!button || !/^\s*submit\s*$/i.test(button.textContent || "")) return;
    const started = Math.floor(Date.now() / 1000) - 10;
    const generation = ++pending;
    report("Waiting for an Accepted submission…");
    (async () => {
      for (let attempt = 0; attempt < 16; attempt++) {
        await delay(4000);
        if (generation !== pending) return;
        const ok = await syncLatest({ after: started });
        if (ok) return;
      }
      if (generation === pending) report("No new Accepted submission detected. Use Sync Accepted after it passes.");
    })();
  }, true);
})();
