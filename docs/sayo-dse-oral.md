# Sayo — DSE English Oral Practice

## Overview
Sayo is a web-based DSE English Oral practice app with AI-powered TTS (text-to-speech) and STT (speech-to-text). It runs at:
- **https://gameworld.zeabur.app/sayo-dse-oral/**

## Architecture

### Frontend (Static HTML/JS)
- **Location:** `mini-games/sayo-dse-oral/index.html`
- **Repo:** `raycoderhk/mini-games`
- **Deploy:** GitHub push → Zeabur auto-deploys

### Backend (Sayo Web — Optional)
- **Location:** `sayo-web/` (Flask + Edge TTS)
- **Status:** Standalone frontend works without it
- **Purpose:** Provides Edge TTS fallback when MiniMax fails

## Features

### 1. 🎲 Random Topic Practice
- Pick a random DSE topic from 20+ topics
- 3 AI candidates (Sarah, Mike, Amy) discuss the topic
- User speaks/ypes answers, AI responds
- Uses Web Speech API (mic) or text input

### 2. 📖 Reading Comprehension
- 5 articles with 4 questions each
- Topics: AI in schools, Digital divide, France social media ban, NASA Artemis, HK students & AI
- Multiple choice with instant feedback

### 3. 🎮 Watch Mock Exam
- **3 different mock exam topics:**
  1. Financial Literacy in Schools
  2. AI Tools in Homework
  3. Country Parks Promotion
- User picks topic before starting (selection screen)
- 32-36 turns per exam, ~8 minutes
- 4 AI candidates: Sarah, Mike, Amy, Ray
- Shows transcript + TTS audio
- Pause/Resume/Stop controls

## TTS Configuration

### MiniMax TTS (Primary)
- **API:** `https://api.minimaxi.com/v1/t2a_v2`
- **Model:** `speech-2.8-hd`
- **Voice IDs:**
  - Sarah: `Cantonese_GentleLady`
  - Mike: `Cantonese_PlayfulMan`
  - Amy: `male-qn-qingse`
- **Retry:** 3 attempts with exponential backoff (500ms → 1s → 2s) on 529 errors
- **Fallback:** Browser Web Speech API if MiniMax fails after retries

### Browser TTS (Fallback)
- Uses `window.speechSynthesis`
- Web Speech API voices (no API key needed)
- Quality varies by browser

## User API Key Storage
- Stored in `localStorage` under `minimax_api_key`
- User enters via Settings ⚙️ button
- Test button validates key before saving

## Data Files
- **Topics:** `src/topics.py` in `sayo/` directory
- **Mock Scripts:** Hardcoded in `index.html` as `MOCK_EXAMS[]` array
- **COMP Articles:** Hardcoded in `index.html` as `COMP[]` array

## Known Issues
- MiniMax free tier rate-limits heavily during HKT daytime (09:00-18:00)
- 529 errors ("server overloaded") are normal on free tier
- Retry logic handles most failures silently
- Browser TTS fallback works but voice quality is lower

## Related Files
| File | Purpose |
|------|---------|
| `mini-games/sayo-dse-oral/index.html` | Main app (this is what's deployed) |
| `sayo/src/topics.py` | Topic definitions (not used by web app) |
| `sayo-web/app.py` | Flask backend (optional, not required) |
| `sayo/src/tts_minimax.py` | MiniMax TTS module |
| `sayo/src/tts_edge.py` | Edge TTS module |
