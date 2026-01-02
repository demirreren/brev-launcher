# Example GPU Project

A minimal GPU-enabled notebook project for demonstrating Brev Launchables.

## Deploy on Brev

[![Deploy on Brev](https://brev.nvidia.com/assets/deploy-badge.svg)](https://brev.nvidia.com/launchables/env-REPLACE_ME/deploy)

> **Note**: Replace `env-REPLACE_ME` with your actual Launchable ID after creating it in the Brev console.

## Local Development

### Prerequisites

- Python 3.10+
- (Optional) PyTorch with CUDA support for GPU testing

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install PyTorch for GPU testing
pip install torch
```

### Run the Notebook

```bash
# Start Jupyter Lab
jupyter lab

# Or Jupyter Notebook
jupyter notebook
```

Open `main.ipynb` and run all cells.

## Run on Brev

### Option 1: Use the Deploy Badge

Click the "Deploy on Brev" badge above (after configuring it with your Launchable ID).

### Option 2: Create a Launchable Manually

1. **Generate the config**:
   ```bash
   # Install brev-launcher
   pip install brev-launcher
   
   # Generate launchable.yaml
   cd example-project
   brev-launcher init
   ```

2. **Create Launchable in Brev Console**:
   - Go to [brev.nvidia.com](https://brev.nvidia.com)
   - Navigate to **Launchables** → **Create Launchable**
   - Select **Git Repository**
   - Click **Show configuration**
   - Paste the contents of `launchable.yaml`

3. **Deploy**:
   - Choose a GPU instance type
   - Click Deploy
   - Wait for the instance to start
   - Open JupyterLab when ready

## What the Notebook Does

1. Prints Python version
2. Checks if PyTorch is installed
3. Checks CUDA/GPU availability
4. Lists available GPUs with names and memory
5. Runs a quick matrix multiplication test on GPU

## Expected Output (on GPU)

```
Python version: 3.10.x
PyTorch version: 2.x.x
CUDA available: True
GPU count: 1
GPU 0: NVIDIA A10G (22.5 GB)
Running quick GPU tensor test...
Matrix multiply result shape: torch.Size([1000, 1000])
✓ GPU test passed!
```

## Troubleshooting

### PyTorch not installed
```bash
pip install torch
```

### CUDA not available
- Ensure you're running on a GPU instance
- Check that CUDA drivers are installed: `nvidia-smi`

### Notebook kernel not found
```bash
pip install ipykernel
python -m ipykernel install --user --name=python3
```

