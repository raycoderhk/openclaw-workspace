# 🔧 Fix for GitHub Actions "Render Keep-Alive" Failure

## ❌ Problem

Your GitHub Actions workflow "Render Keep-Alive" is failing because:

1. **Missing workflow file** - The `.github/workflows/keep-alive.yml` doesn't exist in your repo
2. **Missing secret** - `RENDER_APP_URL` secret is not configured

## ✅ Solution

### Step 1: Create/Update Workflow File

**File:** `.github/workflows/keep-alive.yml`

```yaml
name: Render Keep-Alive

on:
  schedule:
    # Run every 10 minutes to keep Render/Railway app alive
    - cron: '*/10 * * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  ping-render:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render App
        run: |
          echo "Pinging Render app to keep it alive..."
          curl -s -o /dev/null -w "%{http_code}" "${{ secrets.RENDER_APP_URL }}" || echo "Failed to ping"
          
      - name: Check Response
        run: |
          RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${{ secrets.RENDER_APP_URL }}")
          echo "Response code: $RESPONSE"
          if [ "$RESPONSE" -ge 200 ] && [ "$RESPONSE" -lt 400 ]; then
            echo "✅ App is alive!"
            exit 0
          else
            echo "❌ App ping failed with status: $RESPONSE"
            exit 1
          fi
```

### Step 2: Add GitHub Secret

1. Go to: https://github.com/raycoderhk/study-set/settings/secrets/actions
2. Click **"New repository secret"**
3. Add:
   - **Name:** `RENDER_APP_URL`
   - **Value:** Your Render app URL (e.g., `https://your-app.onrender.com`)
4. Click **"Add secret"**

### Step 3: Commit and Push

```bash
# If you have the repo locally
git add .github/workflows/keep-alive.yml
git commit -m "fix: Add Render Keep-Alive workflow"
git push origin main
```

**Or use GitHub UI:**
1. Go to: https://github.com/raycoderhk/study-set
2. Click **"Add file"** → **"Create new file"**
3. Path: `.github/workflows/keep-alive.yml`
4. Paste the workflow content above
5. Click **"Commit changes"**

### Step 4: Verify

1. Go to: https://github.com/raycoderhk/study-set/actions
2. Click **"Render Keep-Alive"** workflow
3. Click **"Run workflow"** (manual trigger)
4. Check if it passes ✅

---

## 📊 Expected Result

After fixing:
- ✅ Workflow runs every 10 minutes
- ✅ Render app stays alive (no sleep mode)
- ✅ No more failure notifications

---

## 🔍 Troubleshooting

**If it still fails:**

1. **Check secret name** - Must be exactly `RENDER_APP_URL`
2. **Check URL format** - Must include `https://`
3. **Check app status** - Make sure your Render app is deployed and running
4. **View logs** - Click on failed run → See exact error message

---

## 📝 Notes

- **Cron syntax:** `*/10 * * * *` = every 10 minutes
- **Workflow dispatch:** Allows manual triggering for testing
- **Exit codes:** 0 = success, 1 = failure (triggers notification)

---

**Created by:** OpenClaw Assistant  
**Date:** 2026-03-08
