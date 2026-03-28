# 🚀 Deployment Reference

**Last updated:** March 28, 2026

---

## Our Deployment Pipeline

### Overview

We deploy via **GitHub → Zeabur** (GitOps pattern). Push to GitHub → Zeabur auto-deploys.

**Key repos:**
- `raycoderhk/mini-games` — Gameworld (HK Places Quiz, GeoBite, other games)
- `raycoderhk/kanban-board` — Kanban + Media Trackers
- `raycoderhk/mission-control` — Mission Control dashboard

---

## How to Deploy a Project

### Step 1: Know where your project lives

```
/home/node/.openclaw/workspace/           ← Main workspace (git repo root)
  hk-places-quiz/                        ← Static HTML games (→ mini-games repo)
  kanban-board/                          ← Kanban backend (→ kanban-board repo)
  kanban-zeabur/                         ← Old Kanban, being replaced
  games/2048-game/                       ← 2048 game (→ 2048-game repo)

/home/node/.openclaw/agents/coding/workspace/projects/  ← Coding agent projects
  gameworld/geobite/                     ← GeoBite (→ mini-games repo subfolder)
```

### Step 2: Copy project to correct location

For static HTML games → place in `workspace/hk-places-quiz/` or create subfolder in `workspace/games/`

### Step 3: Run deploy script

```bash
cd /home/node/.openclaw/workspace
./deploy.sh [gameworld|kanban|all]
```

Or manual:
```bash
cd /home/node/.openclaw/workspace
git add -A
git commit -m "Deploy: <project-name>"
git push origin main
# Zeabur webhook triggers → auto-deploy in ~2-5 minutes
```

### Step 4: Verify

- **Gameworld:** https://gameworld.zeabur.app
- **Kanban:** https://kanban-board.zeabur.app
- **Mission Control:** https://mission-control.zeabur.app

---

## Zeabur Configuration

**Primary domain pattern:** `https://gameworld.zeabur.app/<project-name>/`

**Existing services:**
| Service | URL | Repo | Path |
|---------|-----|------|------|
| Gameworld Home | gameworld.zeabur.app | mini-games | gameworld-zeabur/ |
| HK Places Quiz | gameworld.zeabur.app/hk-places-quiz/ | mini-games | hk-places-quiz/ |
| Kanban Board | kanban-board.zeabur.app | kanban-board | / |
| Mission Control | mission-control.zeabur.app | mission-control | / |

---

## DO: Before Giving Deployment Advice

1. **Read this file first** — `DEPLOYMENT_REFERENCE.md`
2. **Check project location** — `ls /home/node/.openclaw/workspace/` and `ls /home/node/.openclaw/agents/coding/workspace/projects/`
3. **Check existing deploy script** — `cat /home/node/.openclaw/workspace/deploy.sh`
4. **Check Zeabur config** — `cat /home/node/.openclaw/workspace/zeabur-gameworld.json`
5. **Don't assume GitHub Actions** — We push to GitHub and Zeabur auto-deploys via webhook. No separate CI/CD config needed.

## DON'T

- ❌ Don't suggest "link Zeabur to GitHub" as if it's a new setup — it's already configured
- ❌ Don't suggest `npm run build` or `docker` unless the project actually needs it
- ❌ Don't suggest deploying to a new platform without asking
- ❌ Don't make up deployment paths — check the actual directory structure first

---

## Project Structure Reference

```
mini-games repo (raycoderhk/mini-games):
├── gameworld-zeabur/        ← Homepage deploy target
│   └── index.html          ← Main gameworld entry
├── hk-places-quiz/         ← HK Places Quiz (static HTML)
│   ├── index.html
│   └── quiz-data.json
└── geobite/                ← GeoBite game (static HTML)
    └── daily/
        ├── wednesday.html
        ├── thursday.html
        └── friday.html
```

---

## Troubleshooting

**Zeabur not auto-deploying?**
1. Check GitHub → Zeabur webhook is connected
2. Check Zeabur dashboard: https://zeabur.com/dashboard
3. Manual redeploy: Zeabur dashboard → select service → Redeploy

**404 on deployment?**
- Check the domain/path configuration in Zeabur
- Check that `index.html` exists in the deploy root

**Build failed?**
- Most projects are static HTML — no build step needed
- If build needed, check `package.json` scripts

---

*Append any new projects/deployments here as you create them.*
