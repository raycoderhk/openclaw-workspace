# Google Calendar Sync Setup for OpenClaw

**Published:** 2026-06-05  
**Author:** Jarvis (for Raymond)  
**Tags:** #google-calendar #openclaw #automation #python

---

## 🎯 Overview

This guide explains how to set up **Google Calendar sync** for OpenClaw. Your events from HEARTBEAT.md will automatically appear in your iPhone's Google Calendar app.

**Time needed:** 15-20 minutes  
**Cost:** Free (uses Google Free Tier)

---

## 📋 Prerequisites

- OpenClaw installed on your machine
- Google account (same one you use on iPhone)
- Google Calendar app on iPhone (optional but recommended)

---

## 🛠️ Setup Steps

### Step 1: Install Python Dependencies

```bash
cd ~/.openclaw/workspace/skills/google-calendar
pip3 install -r requirements.txt
```

**Requirements:**
- `google-api-python-client>=2.100.0`
- `google-auth-httplib2>=0.1.0`
- `google-auth-oauthlib>=1.0.0`

---

### Step 2: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Select **"NEW PROJECT"**
4. Name it: `OpenClaw Calendar`
5. Click **"CREATE"**
6. Wait for project to create, then select it

---

### Step 3: Enable Google Calendar API

1. In the left sidebar, go to **"APIs & Services"** → **"Library"**
2. Search for: **"Google Calendar API"**
3. Click on it, then click **"ENABLE"**

---

### Step 4: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Choose **"External"** → Click **"CREATE"**

3. Fill in required fields:
   - **App name:** `OpenClaw Calendar`
   - **User support email:** `your-email@gmail.com`
   - **Developer contact:** `your-email@gmail.com`

4. Click **"SAVE AND CONTINUE"**

5. **Scopes:** Click **"ADD OR REMOVE SCOPES"**
   - Check: `https://www.googleapis.com/auth/calendar`
   - Click **"UPDATE"** → **"SAVE AND CONTINUE"**

6. **Test users:** Click **"ADD USERS"**
   - Add: `your-email@gmail.com`
   - Click **"ADD"** → **"SAVE AND CONTINUE"**

---

### Step 5: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name: `OpenClaw Desktop`
5. Click **"CREATE"**
6. **Download the JSON file**
7. Save it as: `credentials.json`
8. Move it to: `~/.openclaw/workspace/skills/google-calendar/credentials.json`

---

### Step 6: Authenticate (First Time Only)

```bash
cd ~/.openclaw/workspace/skills/google-calendar
python3 auth.py
```

**What happens:**
- Browser opens automatically
- Login with your Google account
- Grant Calendar permission
- Token (`token.json`) is saved automatically

**Expected output:**
```
🔐 Starting OAuth flow...
✅ Token saved to token.json

📅 Connected to Google Calendar!
   Primary calendar: your-email@gmail.com

✅ Authentication successful!
```

---

### Step 7: Test Sync

```bash
python3 sync_calendar.py
```

**Expected output:**
```
📅 Starting Google Calendar sync...
📋 Found X events to sync
✅ Created: 匹克球 @ Pickledise on 2026-03-13
...
📊 Sync complete!
```

---

### Step 8: Verify on iPhone

1. Open **Google Calendar** app on iPhone
2. Pull down to refresh
3. You should see your OpenClaw events!

---

## 🔄 Auto-Sync Configuration

The sync runs automatically every heartbeat (~30 minutes during daytime).

To manually trigger a sync:
```bash
python3 sync_calendar.py
```

To check sync status:
```bash
python3 list_calendars.py
```

---

## 📁 File Structure

```
skills/google-calendar/
├── README.md              # User guide
├── SETUP_GUIDE.md         # Quick start
├── auth.py                # OAuth authentication
├── sync_calendar.py       # Main sync script
├── requirements.txt       # Python dependencies
├── credentials.json       # Your OAuth credentials ⬅️ YOU create this
├── token.json             # Auto-generated refresh token ⬅️ Auto-created
└── venv/                  # Python virtual environment
```

---

## 🔒 Security Notes

| File | What it contains | Keep private? |
|------|-----------------|---------------|
| `credentials.json` | OAuth app credentials | ✅ YES |
| `token.json` | Refresh token | ✅ YES |

Both files are in `.gitignore` — **never commit them to git**.

---

## 🐛 Troubleshooting

### "credentials.json not found"
- Download from: Google Cloud Console → APIs & Services → Credentials → OAuth Client ID → Download JSON
- Save as `credentials.json` in the skill folder

### "Token expired"
```bash
rm token.json
python3 auth.py
```

### Events not showing on iPhone
1. Open Google Calendar app
2. Settings → Your account → Sync now
3. Wait 1-2 minutes

### "Access denied" during OAuth
- Make sure you added yourself as a test user
- Go to: OAuth consent screen → Test users → Add your email

---

## 📱 How It Works

```
HEARTBEAT.md                    Google Calendar API
┌──────────────┐               ┌──────────────────┐
│ Events from  │──sync_calendar.py──▶│ Create events  │
│ HEARTBEAT.md │               │ in Google        │
└──────────────┘               └──────────────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ iPhone Google    │
                              │ Calendar App     │
                              └──────────────────┘
```

1. **Reads** HEARTBEAT.md for upcoming events
2. **Parses** event details (date, time, title, location)
3. **Checks** Google Calendar for existing events (avoids duplicates)
4. **Creates** new events via Google Calendar API

---

## 🔧 Event Format in HEARTBEAT.md

The parser recognizes these formats:

```markdown
**3 月 13 日 (星期五)**
• 11:00-13:00 HKT - 匹克球 @ Pickleland
• 19:00 HKT - 家庭晚餐 @ 餐廳名稱
```

Supported patterns:
- Date: `3 月 13 日 (星期五)` or `March 13, 2026`
- Time: `11:00-13:00 HKT` or `19:00 HKT`
- Duration: `11:00-13:00` (2 hours)

---

## 📊 API Quotas

Google Calendar API free tier:
- **1,000,000 requests/day**
- **100 requests/100 seconds/user**

For personal use, you'll never hit these limits.

---

## 📝 Related Files

- `skills/google-calendar/SETUP_GUIDE.md` - Quick reference
- `skills/google-calendar/auth.py` - OAuth script source
- `skills/google-calendar/sync_calendar.py` - Sync script source

---

**Questions?** Ask in OpenClaw Discord #help channel!