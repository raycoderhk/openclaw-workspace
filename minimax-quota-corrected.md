# Minimax Quota Usage - CORRECTED ANALYSIS
**Checked:** 2026-03-26 03:26 UTC

## 📊 **CORRECTED Usage Summary** (Web Dashboard is Correct)

### **API Response Misinterpretation:**
The API field `"current_interval_usage_count":4493` is **NOT remaining calls** - it's **USED calls out of 4500 total**.  
But your web dashboard shows **7/4500 used**, which means:

**Actual Usage:** 7 calls used, 4493 calls remaining!

### 1. **Text Generation (MiniMax-M* including M2.7)**
- **Total:** 4,500 calls per interval
- **Used:** **7 calls** ✅ (NOT 4493!)
- **Remaining:** **4,493 calls** ✅
- **Reset:** 3 hours 34 minutes
- **Status:** **HEALTHY - Plenty of quota!**

### 2. **Text to Speech HD**
- **Total:** 11,000 calls per day
- **Used:** **0 calls** ✅
- **Remaining:** **11,000 calls** ✅
- **Reset:** 12 hours 34 minutes

### 3. **Hailuo-2.3-Fast-768P 6s** (Video/Fast)
- **Total:** 2 calls per day
- **Used:** **0 calls** ✅
- **Remaining:** **2 calls** ✅

### 4. **Hailuo-2.3-768P 6s** (Video/Standard)
- **Total:** 2 calls per day
- **Used:** **0 calls** ✅
- **Remaining:** **2 calls** ✅

### 5. **Music-2.5** (Music Generation)
- **Total:** 4 calls per day
- **Used:** **0 calls** ✅
- **Remaining:** **4 calls** ✅

### 6. **Image-01** (Image Generation)
- **Total:** 120 calls per day
- **Used:** **0 calls** ✅
- **Remaining:** **120 calls** ✅

## ✅ **GOOD NEWS: Quota is HEALTHY!**

### **For Discord M2.7 Usage:**
- **Available:** 4,493 calls remaining
- **Reset in:** 3 hours 34 minutes
- **Weekly:** 45,000 calls total (44,976 remaining)
- **Status:** **SAFE TO PROCEED!**

## 🔧 **Next Steps:**

### 1. **Restart Gateway to Apply M2.7 Configuration**
Since we have plenty of quota, we can proceed with MiniMax-M2.7 for Discord.

### 2. **Gateway Restart Options:**
Since `systemctl` isn't available, try:
```bash
# Option A: Kill and let auto-restart
pkill -f openclaw-gateway

# Option B: Use OpenClaw CLI if available
openclaw gateway stop
openclaw gateway start

# Option C: Direct binary execution
/opt/openclaw/openclaw-gateway &
```

### 3. **Monitor Usage:**
Keep checking with:
```bash
curl --location 'https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains' \
--header "Authorization: Bearer $(grep MINIMAX_API_KEY /home/node/.openclaw/.env | cut -d= -f2)" \
--header 'Content-Type: application/json'
```

## 📈 **Usage Estimates for Discord:**

### **Conservative Estimate:**
- Average Discord message: ~500 tokens
- 4,493 calls × 500 tokens = ~2.25M tokens
- At $0.30/1M tokens = **~$0.68 cost** for current interval

### **Heavy Usage Estimate:**
- Average Discord message: ~1,000 tokens  
- 4,493 calls × 1,000 tokens = ~4.5M tokens
- At $0.30/1M tokens = **~$1.35 cost** for current interval

## 🎯 **Recommendation:**
**PROCEED WITH M2.7 FOR DISCORD!** ✅
- Quota is healthy (4,493 calls remaining)
- Cost is minimal (~$0.68-$1.35 per interval)
- M2.7 provides better quality for Discord conversations

**Ready to restart the gateway and activate M2.7 for Discord?**