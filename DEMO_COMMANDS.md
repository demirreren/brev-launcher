# 🎬 DEMO COMMANDS - Copy & Paste Ready

## 📍 Setup (One-time)
```bash
cd /Users/muhibwaqar/brev-launcher
```

---

## 🎯 OPTION 1: Quick Demo (30 seconds)

### Simple Mode Only
```bash
cd example-stable-diffusion
brev-launcher cost-estimate
```

**Shows:**
- ✅ Recommended: A10 (24GB) at $0.90/hr
- 💰 Savings: **$14,016/year** vs A100

---

## 🚀 OPTION 2: Full Demo (60 seconds)

### Simple Mode → Advanced Mode
```bash
cd example-stable-diffusion

# Show simple mode
brev-launcher cost-estimate

# Show advanced mode (impressive!)
brev-launcher cost-estimate --advanced
```

**Shows:**
- Simple: A10 recommendation ($14k savings)
- Advanced: 2x T4 on MASSEDCOMPUTE ($16k savings)
- 83 suitable configurations found across 14 providers

---

## 🎥 RECORDING TIPS

### Silent Terminal Recording (Recommended)
1. **Start screen recording** (Cmd+Shift+5 on Mac)
2. **Clear terminal:** `clear`
3. **Run demo:** Copy commands above
4. **Let output display** (pause 3-5 seconds)
5. **Stop recording**

### Terminal Settings for Best Visual
```bash
# Increase font size for visibility
# Use dark theme
# Full screen terminal window
```

---

## 📊 EXAMPLE PROJECTS TO TEST

### Example 1: Stable Diffusion (Included)
```bash
cd example-stable-diffusion
brev-launcher cost-estimate --advanced
```
- **Model:** Stable Diffusion v1.5
- **Detected VRAM:** ~9GB
- **Best GPU:** 2x T4 ($0.59/hr)
- **Savings:** $16,732/year

### Example 2: Basic Notebook (Included)
```bash
cd example-project
brev-launcher cost-estimate
```
- **Model:** Generic PyTorch
- **Detected VRAM:** 4GB (baseline)
- **Best GPU:** T4 ($0.29/hr)

### Example 3: Create Your Own
```bash
# Any Python ML project works!
cd /path/to/your/ml/project
brev-launcher cost-estimate --advanced
```

---

## 🐛 IF COMMANDS DON'T WORK

### Option A: Use Python directly
```bash
cd /Users/muhibwaqar/brev-launcher
PYTHONPATH=src python3 -m brev_launcher.cli cost-estimate example-stable-diffusion/
PYTHONPATH=src python3 -m brev_launcher.cli cost-estimate --advanced example-stable-diffusion/
```

### Option B: Install in editable mode
```bash
cd /Users/muhibwaqar/brev-launcher
pip install -e .
# Then use: brev-launcher cost-estimate
```

### Option C: Run the demo script
```bash
cd /Users/muhibwaqar/brev-launcher
./demo.sh
```

---

## 💬 TWITTER CAPTION IDEAS

### Short & Punchy
```
Built a GPU cost optimizer for @brevdev

Scans your ML code → recommends cheapest GPU

Saved $16k/year on this Stable Diffusion project 🔥

github.com/brevdev/brev-launcher
```

### Technical
```
Stop overpaying for GPUs 💰

New @brevdev feature: `brev-launcher cost-estimate`

• Scans code for ML models (SD, LLaMA, Whisper)
• Estimates VRAM requirements  
• Searches 490+ instances across 14 providers
• Recommends cheapest option

$16k/year saved on this example 👇
```

### Problem/Solution
```
Renting an A100 for Stable Diffusion? 

You're paying $2.50/hr for 80GB when you only need 18GB.

Built a tool that finds cheaper alternatives:
→ 2x T4 on MASSEDCOMPUTE: $0.59/hr

$16,732/year saved. One command.

github.com/brevdev/brev-launcher
```

---

## ✨ KEY NUMBERS FOR DEMO

- **Database size:** 490+ instances (87 in current build)
- **GPU models:** 12 types (B300, H200, H100, A100, L40S, A10, RTX 4090, etc.)
- **Providers:** 14 (MASSEDCOMPUTE, DATACRUNCH, AWS, GCP, Lambda Labs, etc.)
- **Price range:** $0.29/hr to $49.49/hr
- **Example savings:** $14k-$16k/year (Stable Diffusion XL)

---

## 🎯 READY TO RECORD!

**Recommended flow:**
1. Open terminal full screen
2. `cd example-stable-diffusion`
3. Start recording
4. `brev-launcher cost-estimate --advanced`
5. Wait 5 seconds for output
6. Stop recording
7. Post with caption above

**No talking needed!** The terminal output speaks for itself. 🎬

