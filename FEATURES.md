# New Features: GPU Detection & Brev Environment Capture

## 🎯 What's New

brev-launcher now captures your **actual Brev environment** and generates configs that match your current setup!

## ✨ Features Added

### 1. **GPU Auto-Detection** 
Automatically detects the GPU you're currently using via `nvidia-smi`:

```bash
🚀 Brev Launcher - Initialize Launchable Config

Scanning project...
✓ Git repository: https://github.com/demirreren/brev-launcher
✓ GPU detected: gpu_1x_a10 (24.0GB VRAM)
```

**Supported GPUs:**
- A10 → `gpu_1x_a10`
- A100 → `gpu_1x_a100` / `gpu_1x_a100_80gb`
- T4 → `gpu_1x_t4`
- V100 → `gpu_1x_v100`
- H100 → `gpu_1x_h100`

### 2. **Smart GPU Config Generation**

**Before:**
```yaml
compute:
  gpu: any
  note: Select lowest-cost GPU in Brev UI
```

**After (when running on A10):**
```yaml
compute:
  gpu: gpu_1x_a10
  note: Auto-detected from current instance (24.0GB VRAM)
```

### 3. **Enhanced Brev Instance Detection**

Now captures:
- Instance name
- GPU type
- GPU memory size
- Instance status

### 4. **Git Optional Mode**

Can now run without a git repository (useful for testing inside Brev instances). The tool will prompt you to continue and generate a template config.

## 🎬 Demo Flow

### Inside a Brev GPU Instance:

```bash
# 1. SSH into your Brev A10 instance
ssh your-instance.brev.dev

# 2. Clone your project
git clone https://github.com/YOUR_USERNAME/YOUR_REPO
cd YOUR_REPO

# 3. Install brev-launcher
pip install -e /path/to/brev-launcher

# 4. Run the tool
brev-launcher init

# Output:
# 🚀 Brev Launcher - Initialize Launchable Config
# 
# Scanning project...
# ✓ Git repository: https://github.com/YOUR_USERNAME/YOUR_REPO
# ✓ Default branch: main
# ✓ Dependencies: requirements.txt
# ✓ Entry file: app.py
# ✓ GPU detected: gpu_1x_a10 (24.0GB VRAM)
# 
# Generating configuration...
# ✓ Written: launchable.yaml
```

### Generated `launchable.yaml`:

```yaml
name: your-project
description: your-project - deployed via Brev Launchables
source:
  type: git
  url: https://github.com/YOUR_USERNAME/YOUR_REPO
  ref: main
  path: /
runtime:
  mode: vm
  setup:
    python_version: '3.10'
    install: pip install -r requirements.txt
  start:
    webapp:
      command: python app.py
      port: 7860
compute:
  gpu: gpu_1x_a10  # ← Auto-detected!
  note: Auto-detected from current instance (24.0GB VRAM)
networking:
  ports:
    - 7860
files:
  include:
    - .
metadata:
  generated_by: brev-launcher
  generated_at: '2026-01-02T20:00:00+00:00'
```

## 💡 Use Cases

### 1. **Share Your Exact Environment**
Working on a project in Brev? Run `brev-launcher init` to generate a config that captures your exact GPU setup. Share it with teammates so they get the same environment.

### 2. **Optimize GPU Selection**
The tool shows you which GPU you're currently using. If your app works well on a T4, the generated config will specify T4, saving costs vs defaulting to "any".

### 3. **Environment Documentation**
The generated YAML serves as documentation of your exact working environment (GPU, Python version, dependencies, commands).

## 🚀 Value Proposition

**Before brev-launcher:**
- Manually write YAML config
- Guess which GPU to use
- Trial and error to find right settings

**After brev-launcher:**
- One command captures everything
- GPU auto-detected from current environment
- Share exact working setup with one file

## 📋 Technical Details

### Files Modified:
- `src/brev_launcher/detect.py` - Added `detect_current_gpu()` and `get_gpu_memory_gb()`
- `src/brev_launcher/project_scan.py` - Enhanced `BrevInfo` dataclass and `check_brev_cli()`
- `src/brev_launcher/launchable_schema.py` - Added `with_gpu()` method
- `src/brev_launcher/cli.py` - Integrated GPU detection, added git-optional mode

### New Functions:
```python
def detect_current_gpu() -> str:
    """Detect GPU type from nvidia-smi."""
    # Maps GPU names to Brev GPU types

def get_gpu_memory_gb() -> Optional[float]:
    """Get GPU memory in GB from nvidia-smi."""
    # Returns VRAM size
```

## 🎯 Next Steps

To make this a complete "Brev Launchable Sharer":

1. ✅ **GPU Detection** - Done!
2. ✅ **Brev Instance Metadata** - Done!
3. ✅ **Git Optional Mode** - Done!
4. 🔲 **Direct Deploy Links** - Generate shareable URLs
5. 🔲 **Web UI** - Create a simple web interface
6. 🔲 **Brev API Integration** - Auto-create Launchables via API

## 📸 Demo Ready

This is now ready to demo! Key improvements:
- Shows actual GPU detection in terminal output
- Generates configs that match real environments
- Works inside Brev instances
- Perfect for the "Brev Environment Sharer" pitch

---

**Built for the Brev community** 🚀

