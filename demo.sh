#!/bin/bash
# BREV-LAUNCHER COST OPTIMIZER DEMO
# Record this for your Twitter post!

clear

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║              BREV-LAUNCHER GPU COST OPTIMIZER DEMO                 ║"
echo "║                  30-Second Twitter Recording                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Goal: Show how much $$$ you can save on GPU costs"
echo ""

# Pause for effect
sleep 2

echo "📂 Let's analyze our Stable Diffusion project..."
echo ""
sleep 1

# Navigate to example project
cd example-stable-diffusion

echo "$ brev-launcher cost-estimate"
echo ""
sleep 1

# Run simple mode (uses PYTHONPATH since we may not have installed version)
PYTHONPATH=../src python3 -c "
from brev_launcher.cli import app
import sys
sys.argv = ['brev-launcher', 'cost-estimate', '.']
app()
" 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sleep 2

echo "💡 Want more options? Try ADVANCED mode..."
echo ""
sleep 1

echo "$ brev-launcher cost-estimate --advanced"
echo ""
sleep 1

PYTHONPATH=../src python3 -c "
from brev_launcher.cli import app
import sys
sys.argv = ['brev-launcher', 'cost-estimate', '--advanced', '.']
app()
" 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ DEMO COMPLETE!"
echo ""
echo "💰 Key Takeaway: Save \$14k-\$16k/year by choosing the right GPU!"
echo ""
echo "🔗 Try it yourself: github.com/brevdev/brev-launcher"
echo ""

