# Raymond's Deployed Projects Overview

**Last Updated:** 2026-03-27  
**Author:** Jarvis (AI Assistant for Raymond)

---

## Quick Comparison Table

| Project | URL | Purpose | Tech Stack | Auth |
|---------|-----|---------|------------|------|
| **Kanban Board** | kanban-board.zeabur.app | Personal task management | Node.js + Express + JSON | Google OAuth |
| **Mission Control** | mission-control.zeabur.app | Productivity dashboard | Next.js + Supabase | Google OAuth |
| **Study Set App** | kanban-board.zeabur.app/public/study-set.html | Study flashcards | HTML/CSS/JS + LocalStorage | None (public) |
| **Magazine App** | kanban-board.zeabur.app/magazine/ | Magazine reader | HTML/CSS/JS + JSON | Google OAuth (learning center) |
| **Movie Tracker** | kanban-board.zeabur.app/public/movies.html | Track movies watched | HTML/CSS/JS + JSON | None (public) |
| **Book Tracker** | kanban-board.zeabur.app/public/index.html | Track books reading | HTML/CSS/JS + JSON | None (public) |
| **TV Series Tracker** | kanban-board.zeabur.app/public/series.html | Track TV series | HTML/CSS/JS + JSON | None (public) |
| **GameWorld Mini Games** | gameworld.zeabur.app/ | Mini games collection | Next.js | None (public) |
| **Pickleball Polymarket** | gameworld.zeabur.app/pickleball-polymarket/ | Prediction game | Next.js | None (public) |
| **Nutritionist App** | nutrition-app.zeabur.app | Food image recognition | Python + FastAPI + Vision AI | None |

---

## Detailed Project Descriptions

### 1. Kanban Board 🎯
**URL:** https://kanban-board.zeabur.app  
**GitHub:** github.com/raycoderhk/kanban-board

**What it does:**
- Personal task management (like Trello)
- Track tasks with status: To Do → In Progress → Done
- Google OAuth login (each user sees only their tasks)
- Tasks stored in Supabase database

**Tech Stack:**
- Frontend: Vanilla HTML/CSS/JavaScript
- Backend: Node.js + Express
- Database: Supabase (PostgreSQL)
- Auth: Google OAuth 2.0
- Hosting: Zeabur

**When helping:**
- User can't login → Check Supabase connection + Google OAuth config
- Tasks not saving → Check Supabase database + RLS policies

---

### 2. Mission Control 🚀
**URL:** https://mission-control.zeabur.app  
**GitHub:** github.com/raycoderhk/mission-control

**What it does:**
- Productivity dashboard
- Goals tracking
- Events management
- Friends list
- Similar to Notion dashboard

**Tech Stack:**
- Framework: Next.js 14
- Auth: NextAuth.js (Google OAuth)
- Database: Supabase
- Hosting: Zeabur

**When helping:**
- Same issues as Kanban Board (Supabase + OAuth)

---

### 3. Study Set App 📚
**URL:** https://kanban-board.zeabur.app/public/study-set.html  
**Part of:** Kanban Board repo

**What it does:**
- Flashcard-style study app
- User can create study sets with terms/definitions
- Quiz mode to test knowledge
- Progress tracking

**Tech Stack:**
- Pure HTML/CSS/JavaScript
- LocalStorage for data persistence
- No backend/auth needed

**When helping:**
- Data not saving → Clear browser cache/localStorage
- UI issues → Check HTML structure

---

### 4. Magazine App 📰
**URL:** https://kanban-board.zeabur.app/magazine/  
**Part of:** Kanban Board repo

**What it does:**
- Read magazines ( Economist, Bloomberg, National Geographic, HK Economic Journal)
- Learning center with study materials
- Progress tracking for learning

**Tech Stack:**
- Frontend: Vanilla HTML/CSS/JavaScript
- Content: JSON files (public/*.json)
- Auth: Google OAuth for learning center (optional)

**When helping:**
- Magazine not loading → Check JSON file exists
- Can't save progress → Check Google OAuth

---

### 5. Media Trackers (Movies/Books/TV) 🎬📚📺
**URLs:**
- Movies: https://kanban-board.zeabur.app/public/movies.html
- Books: https://kanban-board.zeabur.app/public/index.html  
- TV Series: https://kanban-board.zeabur.app/public/series.html

**What they do:**
- Track personal media consumption
- Add ratings, notes, watch/read status
- Search and filter functionality
- Cover images

**Tech Stack:**
- Pure HTML/CSS/JavaScript
- JSON files for data storage
- No auth needed (public access)

**When helping:**
- Can't add item → Check JSON file permissions
- Images not showing → Check public/ folder

---

### 6. GameWorld Mini Games 🎮
**URL:** https://gameworld.zeabur.app/  
**GitHub:** (private repo)

**What it does:**
- Collection of mini games
- Including Pickleball Polymarket
- Fun/property prediction games

**Tech Stack:**
- Next.js
- No auth needed
- Hosting: Zeabur

**When helping:**
- Game not loading → Check deployment logs
- 404 errors → Check routing configuration

---

### 7. Pickleball Polymarket 🏓
**URL:** https://gameworld.zeabur.app/pickleball-polymarket/  
**Part of:** GameWorld repo

**What it does:**
- Prediction market for pickleball games
- Users can place predictions on game outcomes
- Score tracking

**Tech Stack:**
- Next.js
- No auth
- Deployed as subdirectory of GameWorld

**When helping:**
- Same as GameWorld

---

### 8. Nutritionist App 🥗
**URL:** https://nutrition-app.zeabur.app  
**(Private repo)**

**What it does:**
- Food image recognition
- Upload photo of food → AI analyzes nutrition
- Uses MiniMax Vision AI (abab6.5s-vision model)
- Calorie tracking

**Tech Stack:**
- Backend: Python + FastAPI
- AI: OpenRouter MiniMax-01 Vision (or Aliyun)
- Hosting: Zeabur

**When helping:**
- Image recognition not working → Check MiniMax API key + quota
- Server errors → Check FastAPI logs

---

## Architecture Patterns (Reusable)

### Google OAuth + Supabase Pattern
Used by: Kanban Board, Mission Control

**User Flow:**
1. User clicks "Login with Google"
2. NextAuth handles OAuth
3. Email stored in Supabase as user identifier
4. RLS policies ensure data isolation

**Database Schema:**
- `users` table (email, name, avatar)
- Each app has its own table (tasks, events, goals)
- RLS enabled for security

### JSON Storage Pattern
Used by: Study Sets, Media Trackers, Magazine

**Storage:**
- Public JSON files in `public/` folder
- Browser localStorage for user-specific data
- No backend needed

### API + AI Pattern
Used by: Nutritionist App

**Flow:**
1. User uploads image
2. API sends to AI vision model
3. AI returns nutrition analysis
4. Display to user

---

## Common Issues & Solutions

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Login broken | Google OAuth expired | Re-authenticate in Supabase |
| Tasks not saving | Supabase RLS issue | Check row-level security policies |
| JSON not loading | File missing/path wrong | Check public/ folder + file name |
| AI not working | MiniMax quota exhausted | Check quota with minimax-quota-check |
| Deployment failed | Build error | Check Zeabur logs + package.json |

---

## How to Identify Which Project

**Ask the user:**
1. What's the URL? (check table above)
2. What were you trying to do?
3. What happened?

**Quick diagnosis by URL:**
- `kanban-board.zeabur.app` → Kanban Board ecosystem
- `mission-control.zeabur.app` → Mission Control
- `gameworld.zeabur.app` → GameWorld
- `nutrition-app.zeabur.app` → Nutritionist App

---

## Contact

- **Raymond** → For project questions/changes
- **Jarvis (in #skills)** → For technical help/troubleshooting
- Check project's README.md → For specific setup instructions

---

*Maintained by Jarvis. Last updated: 2026-03-27*
