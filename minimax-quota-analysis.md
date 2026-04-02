# Minimax Quota Usage Analysis
**Checked:** 2026-03-26 03:24 UTC

## 📊 Current Usage Summary

### 1. **MiniMax-M* (Text Models - M2.7, etc.)**
- **Current Interval:** 4,500 calls total
- **Used:** 4,493 calls
- **Remaining:** **7 calls** ⚠️
- **Weekly Total:** 45,000 calls
- **Weekly Used:** 44,976 calls
- **Weekly Remaining:** **24 calls** ⚠️

### 2. **Speech-HD (Voice Synthesis)**
- **Current Interval:** 11,000 calls total
- **Used:** 11,000 calls
- **Remaining:** **0 calls** ❌
- **Weekly Total:** 77,000 calls
- **Weekly Used:** 77,000 calls
- **Weekly Remaining:** **0 calls** ❌

### 3. **MiniMax-Hailuo-2.3-Fast-6s-768p** (Video/Fast)
- **Current Interval:** 2 calls total
- **Used:** 2 calls
- **Remaining:** **0 calls** ❌

### 4. **MiniMax-Hailuo-2.3-6s-768p** (Video/Standard)
- **Current Interval:** 2 calls total
- **Used:** 2 calls
- **Remaining:** **0 calls** ❌

### 5. **Music-2.5** (Music Generation)
- **Current Interval:** 4 calls total
- **Used:** 4 calls
- **Remaining:** **0 calls** ❌

### 6. **Image-01** (Image Generation)
- **Current Interval:** 120 calls total
- **Used:** 120 calls
- **Remaining:** **0 calls** ❌

## ⚠️ **CRITICAL ALERT: Text Model Quota**

**You have only 7 calls remaining in the current interval for MiniMax-M* models!**

This includes:
- MiniMax-M2.7 (what we just configured for Discord)
- MiniMax-M2.7-highspeed
- MiniMax-M2.5
- Other M-series text models

## 🚨 **Immediate Actions Required:**

1. **Check billing/plan:** Visit https://platform.minimaxi.com
2. **Consider upgrading** if you plan to use Discord heavily with M2.7
3. **Monitor usage closely** - Discord will stop working when quota is exhausted
4. **Alternative:** Switch Discord back to DeepSeek temporarily using rollback script

## 💡 **Recommendations:**

### Option A: Upgrade Plan
- Check current plan at https://platform.minimaxi.com/pricing
- M2.7 Token Plan Plus (179 RMB/year) gives 90% discount
- Ensure it includes sufficient API calls for Discord usage

### Option B: Hybrid Approach
- Keep Discord on M2.7 but monitor usage
- Set up alerts when quota is low
- Have rollback script ready

### Option C: Conservative Usage
- Use M2.7 only for important Discord conversations
- Consider switching less critical channels back to DeepSeek

## 🔧 **Technical Notes:**
- **API Key:** Valid and working
- **Current Interval:** Based on timestamps, appears to be daily/hourly limits
- **Weekly Reset:** Weekly limits also nearly exhausted
- **Vision Model:** Not listed in quota - may have separate billing

## 📋 **Next Steps:**
1. **Check your Minimax dashboard:** https://platform.minimaxi.com
2. **Review current plan and upgrade if needed**
3. **Decide whether to proceed with M2.7 for Discord**
4. **If proceeding, restart gateway:** `openclaw gateway restart`
5. **Monitor usage closely** with the curl command above

## ⏰ **Timestamps Analysis:**
- **Start Time:** 1774490400000 (Unix milliseconds)
- **End Time:** 1774508400000 (Unix milliseconds)
- **Remaining Time:** 12,925,184 ms ≈ **3.6 hours** until reset
- **Weekly Reset:** ~304,525,184 ms ≈ **3.5 days** until weekly reset

**You have about 3.6 hours until the current interval resets!**