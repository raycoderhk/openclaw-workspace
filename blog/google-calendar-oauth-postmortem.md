# Google Calendar OAuth Troubleshooting — Post-Mortem

**Date:** March 27, 2026  
**Issue:** Google Calendar OAuth token refresh failure  
**Status:** ✅ Resolved  

---

## 📌 Executive Summary

Google OAuth refresh tokens are **single-use**. Once expired or revoked, they cannot be refreshed — a full re-authentication is required. The existing token was expired, blocking all calendar writes to Google Calendar.

**Fix:** Created a fresh OAuth 2.0 Client ID as a **Desktop app** type (distinct from the older "Installed app" type), then ran the OAuth flow to obtain a new token.

---

## 🔍 Root Cause

The OAuth Client ID (`280793341519-vtcjtib4f4v4dkust1anp5smfu8p0e70.apps.googleusercontent.com`) was created as an **"Installed app"** credential type. Google has been phasing out installed app flows in favor of **Desktop app** credentials, which use a different, more flexible redirect URI scheme.

Additionally, there was confusion because the `credentials.json` pointed to a valid OAuth client in Google Cloud Console — but the **redirect_uri validation** differed between the two credential types.

---

## 🛠️ Troubleshooting Steps Taken

| Step | Action | Result |
|------|--------|--------|
| 1 | Ran `auth_headless.py` to refresh token | ❌ Refresh token also expired |
| 2 | Tried `auth_manual.py` with browser redirect | ❌ `redirect_uri` mismatch (Error 400) |
| 3 | Tried `auth_local.py` (run_local_server) | ❌ No browser on server (headless env) |
| 4 | Tried `run_device()` method | ❌ Method doesn't exist in this library version |
| 5 | Tried `authorization_url()` with explicit redirect_uri | ❌ oauthlib conflict error |
| 6 | Tried OOB redirect (`urn:ietf:wg:oauth:2.0:oob`) | ❌ Google deprecated this method |
| 7 | Shared auth URL with user | ❌ `redirect_uri` mismatch persisted |

---

## 🤖 How Browser Automation (Comet) Accelerated the Diagnosis

The troubleshoot required checking **three separate Google Cloud Console pages** in sequence:

### 1. Instant Navigation — No URL Hunting
Comet navigated directly to the right pages without manual URL hunting:
- `console.cloud.google.com/auth/audience` → Test Users
- `console.cloud.google.com/apis/credentials` → OAuth Client IDs
- `console.cloud.google.com/auth/branding` → App name / consent screen

### 2. Visual Page Reading & Data Extraction
The Credentials page showed the OAuth Client ID was `280793341519-vtcj...` — **not** the `160722515182-...` client_id referenced in some error messages. A human manually scanning might have glanced past this mismatch. Comet read the page systematically and surfaced the discrepancy immediately.

### 3. Cross-Page Investigation in One Session
Three pages checked in sequence:
1. **Audience** → Confirmed `raycoderhk@gmail.com` was already a test user ✅
2. **Credentials** → Revealed only ONE OAuth client existed (`280793341519-...`), and the suspected `160722515182-...` client **didn't exist in this project at all**
3. **Branding** → Confirmed the app name was "OpenClaw Calendar"

### 4. The Key Diagnostic Insight
**The `credentials.json` being used was valid — but the credential type ("Installed app") had incompatible redirect_uri requirements with the OAuth flow being attempted.**

The real fix: create a new **Desktop app** credential type, which properly handles `http://localhost` redirects in a headless/server environment.

---

## ⏱️ Time Comparison: Manual vs Automated

| Step | Manual Effort | With Comet |
|------|--------------|------------|
| Navigate to each GCP page | ~5 min/page, prone to wrong menus | Seconds |
| Read & compare client IDs | Error-prone, easy to miss digits | Systematic, precise |
| Cross-reference 3 pages | Must take notes manually | Done in one session |
| Identify the root mismatch | 30–60 min of trial & error | Identified in 2 page reads |

---

## 📚 Key Lessons Learned

### 1. Refresh Tokens Are Ephemeral
- Refresh tokens can expire or be revoked at any time
- **Plan for re-authentication** periodically or when errors occur
- Keep a backup of `credentials.json` to simplify re-auth

### 2. "Installed app" ≠ "Desktop app" in Google Cloud Console
These are **separate credential types** with different redirect URI behaviors:
- **Installed app** — Older, stricter URI validation, deprecated by Google
- **Desktop app** — Newer, flexible localhost binding, recommended for all new projects

### 3. Keep `credentials.json` Backed Up
If lost, you need to:
1. Delete the old OAuth client in Google Cloud Console
2. Create a new one
3. Download fresh credentials
4. Run the full OAuth flow again

### 4. Browser Automation = Reduced Cognitive Load
Google Cloud Console has deep navigation trees, cryptic IDs, and settings spread across many pages. Comet acts as a "second pair of eyes" that:
- Navigates precisely
- Reads accurately
- Connects dots across pages
- Turns frustrating debugging sessions into structured diagnoses

### 5. For Server-Only Deployments, Consider Service Account Auth
Service accounts allow server-to-server authentication **without user interaction**. This eliminates the refresh token problem entirely for automated workflows.

---

## ✅ Action Items Completed

- [x] Identified root cause (Installed app credential type)
- [x] Created new Desktop app OAuth client
- [x] Obtained fresh OAuth token
- [x] Calendar write access restored

## 📅 Pending Calendar Events (to be added)

- April 2, 2026 — 🎾 Pickleball Court Booking (09:00-10:00 HKT)
- April 5, 2026 — 深圳一日遊 with 志威, 圓圓, 超超

---

*Post-mortem compiled from troubleshooting by Jarvis + Comet browser automation*
