# 🎨 Stable Diffusion Demo on Brev

A production-ready Stable Diffusion web app with Gradio UI, optimized for GPU deployment on Brev.

[![Deploy on Brev](https://brev.nvidia.com/assets/deploy-badge.svg)](https://brev.nvidia.com/launchables/env-REPLACE_ME/deploy)

## Features

- 🎨 Text-to-image generation with Stable Diffusion v1.5
- 🚀 GPU-optimized with automatic device detection
- 🎛️ Adjustable inference steps and guidance scale
- 💡 Built-in example prompts
- 📱 Beautiful Gradio web interface

## Quick Start (Local)

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended: 8GB+ VRAM)
- 10GB+ disk space for model weights

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (this will download ~4GB of model weights on first run)
pip install -r requirements.txt

# Run the app
python app.py
```

Open http://localhost:7860 in your browser.

## Deploy on Brev (Recommended)

Get instant access to powerful GPUs without any setup!

### Method 1: One-Click Deploy

1. Click the "Deploy on Brev" badge above (after configuring with your Launchable ID)
2. Choose a GPU (A10 or better recommended)
3. Wait 2-3 minutes for deployment
4. Start generating images!

### Method 2: Manual Configuration

1. **Generate config** (if not already present):
   ```bash
   pip install brev-launcher
   cd example-stable-diffusion
   brev-launcher init --type webapp --port 7860
   ```

2. **Create Launchable**:
   - Go to [brev.nvidia.com](https://brev.nvidia.com)
   - Navigate to **Launchables** → **Create Launchable**
   - Select **Git Repository**
   - Paste the contents of `launchable.yaml`

3. **Deploy**:
   - Choose GPU: A10 (16GB) or better
   - Wait for deployment
   - Access your web app via the provided URL

## Recommended GPU Options

| GPU | VRAM | Speed | Best For |
|-----|------|-------|----------|
| A10 | 24GB | Fast | Production, multiple users |
| T4 | 16GB | Medium | Development, single user |
| A100 | 40GB | Fastest | High-throughput, batching |

## Usage Tips

- **Prompt quality matters**: Be specific and descriptive
- **Inference steps**: 25-30 is a good balance (more = higher quality but slower)
- **Guidance scale**: 7-8 for realistic images, 10+ for more creative interpretations
- **Negative prompts**: Add unwanted elements (e.g., "blurry, low quality")

## Example Prompts

```
A majestic lion in a cyberpunk city, neon lights, highly detailed, 4k

An astronaut riding a horse on Mars, photorealistic, red landscape

A cozy coffee shop interior, warm lighting, plants, wooden furniture

A dragon flying over a medieval castle at sunset, fantasy art
```

## Troubleshooting

### Out of memory errors
- Reduce image size in the code (default is 512x512)
- Use fewer inference steps
- Enable `pipe.enable_sequential_cpu_offload()` for low-VRAM GPUs

### Slow generation on CPU
- Deploy on Brev for GPU access!
- CPU generation takes 5-10 minutes per image

### Model download fails
- Check internet connection
- Model is ~4GB, ensure sufficient bandwidth
- Alternatively, pre-download: `huggingface-cli download runwayml/stable-diffusion-v1-5`

## Tech Stack

- **Stable Diffusion v1.5** - Image generation model
- **Gradio** - Web interface
- **PyTorch** - Deep learning framework
- **Diffusers** - HuggingFace library for diffusion models

## License

This example is MIT licensed. Note that Stable Diffusion v1.5 has its own license terms.

---

Built with ❤️ for the GPU development community. Powered by [Brev](https://brev.nvidia.com).

