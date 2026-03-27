# Deployment Guide - How to Deploy Projects to Zeabur

**Last Updated:** 2026-03-27  
**Author:** Jarvis (AI Assistant for Raymond)

---

## Overview

This guide documents how to deploy web projects to Zeabur hosting platform.

## How Jarvis Deploys Projects

Jarvis uses **GitHub + Zeabur Dashboard** approach:

### Step 1: Prepare Project on GitHub
```
1. Create or update project files in ~/clawd/workspace/projects/<project-name>/
2. Push to GitHub:
   cd ~/clawd/workspace/projects/<project-name>
   git add .
   git commit -m "deployment commit"
   git push origin main
```

### Step 2: Deploy via Zeabur Dashboard
```
1. Go to https://zeabur.com
2. Login (Raymond's account - credentials in password manager)
3. Click "New Project" → "Deploy from GitHub"
4. Select the repository
5. Configure environment variables if needed
6. Deploy!
```

### Step 3: Update Project URL
After deployment, update the project URL in:
- `HEARTBEAT.md` (if it's an event-related project)
- `MEMORY.md` (if it's a significant project)
- Project's own README.md

---

## Required Credentials

### GitHub
- **Account:** raycoderhk (GitHub organization: github.com/raycoderhk)
- **Token:** Available in environment variable or password manager
- **CLI:** `gh` command should work if token is set

### Zeabur
- **Dashboard:** https://zeabur.com
- **Login:** Raymond's account (email in password manager)
- **Note:** CLI (`zb`) requires browser login, so use Dashboard instead

### Environment Variables for Deployment
Common ones needed:
- `DATABASE_URL` - Supabase/postgres connection strings
- `API_KEY` - External API keys (MiniMax, OpenAI, etc.)
- `NEXTAUTH_SECRET` - NextAuth authentication secret

---

## Project Structure Best Practices

```
projects/<project-name>/
├── README.md          # Project description + deployment URL
├── .env.example      # Template for environment variables
├── package.json      # Node.js project (if applicable)
├── src/              # Source code
├── public/           # Static files
└── zeabur.json       # (optional) Zeabur config
```

---

## Troubleshooting

### "gh: command not found"
GitHub CLI not installed in sandbox. **Workaround:**
- Use GitHub web UI to commit/push
- Or push code from local machine
- Document that `gh` needs to be installed in sandbox

### "zb: command not found"
Zeabur CLI requires browser login. **Use Dashboard instead.**

### Environment Variables Not Set
1. Check `.env.example` in project
2. Set variables in Zeabur Dashboard → Project → Settings → Environment Variables
3. Redeploy after adding variables

### Deployment Failed
1. Check Zeabur dashboard for error logs
2. Common issues:
   - Build command failing (check package.json scripts)
   - Missing dependencies (run `npm install` locally first)
   - Wrong build output directory

---

## Quick Reference: Deploy a Node.js Project

```bash
# 1. Clone/push project to GitHub
git clone https://github.com/raycoderhk/<project-name>.git
cd <project-name>

# 2. Make changes
# ... edit files ...

# 3. Push to GitHub
git add .
git commit -m "updates"
git push origin main

# 4. Deploy in Zeabur Dashboard
# https://zeabur.com → Deploy from GitHub → Select repo

# 5. Wait for deployment (~2-3 minutes)
# Check status in Zeabur dashboard
```

---

## Quick Reference: Deploy a Python/FastAPI Project

Same as above, but check:
- `requirements.txt` exists and has all dependencies
- `main.py` or `app.py` is the entry point
- Port setting (usually 8000 or 3000)

---

## Projects Documentation

| Project | URL | GitHub | Notes |
|---------|-----|--------|-------|
| IPO Tracker | gameworld.zeabur.app/ipo-tracker/ | github.com/raycoderhk/mini-games | Static HTML + MiniMax AI |
| Kanban Board | kanban-board.zeabur.app | github.com/raycoderhk/kanban-board | Node.js + Express |
| Mission Control | mission-control.zeabur.app | github.com/raycoderhk/mission-control | Next.js |
| Nutritionist App | nutrition-app.zeabur.app | (private) | Python + FastAPI |
| Pickleball Polymarket | gameworld.zeabur.app/pickleball-polymarket/ | github.com/raycoderhk/mini-games | Next.js |

### Mini-Games Repo Deployment (gameworld.zeabur.app)

For projects under `github.com/raycoderhk/mini-games`:

```
1. Add project files to: games/<project-name>/
2. Ensure .gitignore does NOT ignore games/
3. Git add -f games/<project-name>/
4. Git commit && git push
5. GitHub Actions triggers Zeabur deploy hook
6. Zeabur auto-deploys to: gameworld.zeabur.app/<project-name>/
```

**Important:** If `games/` is gitignored, use `git add -f` to force add.

---

## Questions?

If this guide doesn't help, ask Raymond or check the project README.md.
If deployment still fails, tag Jarvis in #skills channel!

---

*This guide is maintained by Jarvis. Last updated: 2026-03-27*
