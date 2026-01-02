"""GPU pricing and cost estimation for Brev deployments."""

from typing import Dict, Optional

# Brev GPU pricing (as of 2024)
GPU_PRICING: Dict[str, Dict] = {
    "gpu_1x_t4": {
        "name": "T4",
        "vram_gb": 16,
        "cost_per_hour": 0.40,
        "good_for": "Small models, inference, cost-sensitive workloads",
        "compute_score": 60,  # Relative performance score
    },
    "gpu_1x_a10": {
        "name": "A10",
        "vram_gb": 24,
        "cost_per_hour": 0.90,
        "good_for": "Medium models, training, balanced performance",
        "compute_score": 100,
    },
    "gpu_1x_v100": {
        "name": "V100",
        "vram_gb": 16,
        "cost_per_hour": 1.50,
        "good_for": "Legacy workloads, specific library requirements",
        "compute_score": 80,
    },
    "gpu_1x_a100": {
        "name": "A100",
        "vram_gb": 40,
        "cost_per_hour": 2.50,
        "good_for": "Large models, fast training, production workloads",
        "compute_score": 200,
    },
    "gpu_1x_a100_80gb": {
        "name": "A100 80GB",
        "vram_gb": 80,
        "cost_per_hour": 3.00,
        "good_for": "Very large models, massive batch sizes",
        "compute_score": 220,
    },
    "gpu_1x_h100": {
        "name": "H100",
        "vram_gb": 80,
        "cost_per_hour": 4.00,
        "good_for": "Cutting-edge research, fastest training",
        "compute_score": 300,
    },
    "any": {
        "name": "Any GPU",
        "vram_gb": 16,
        "cost_per_hour": 0.60,
        "good_for": "Flexible, Brev will assign available GPU",
        "compute_score": 70,
    },
}


def calculate_monthly_cost(hourly_cost: float, hours_per_day: int = 24) -> float:
    """Calculate monthly cost from hourly rate.
    
    Args:
        hourly_cost: Cost per hour in dollars.
        hours_per_day: Hours of usage per day (default: 24 for always-on).
        
    Returns:
        Monthly cost in dollars.
    """
    return hourly_cost * hours_per_day * 30


def calculate_yearly_cost(hourly_cost: float, hours_per_day: int = 24) -> float:
    """Calculate yearly cost from hourly rate.
    
    Args:
        hourly_cost: Cost per hour in dollars.
        hours_per_day: Hours of usage per day (default: 24 for always-on).
        
    Returns:
        Yearly cost in dollars.
    """
    return hourly_cost * hours_per_day * 365


def get_gpu_info(gpu_type: str) -> Optional[Dict]:
    """Get pricing info for a GPU type.
    
    Args:
        gpu_type: GPU type identifier (e.g., 'gpu_1x_a10').
        
    Returns:
        Dictionary with GPU info, or None if not found.
    """
    return GPU_PRICING.get(gpu_type)


def recommend_gpu(estimated_vram_gb: float, current_gpu: Optional[str] = None) -> Dict:
    """Recommend optimal GPU based on VRAM requirements.
    
    Args:
        estimated_vram_gb: Estimated VRAM requirement in GB.
        current_gpu: Current GPU type (optional).
        
    Returns:
        Dictionary with recommendation details.
    """
    # Add 20% buffer for safety
    required_vram = estimated_vram_gb * 1.2
    
    # Find GPUs that fit
    suitable_gpus = []
    for gpu_id, info in GPU_PRICING.items():
        if gpu_id == "any":
            continue
        if info["vram_gb"] >= required_vram:
            suitable_gpus.append({
                "gpu_id": gpu_id,
                "info": info,
                "cost_efficiency": info["compute_score"] / info["cost_per_hour"],
            })
    
    if not suitable_gpus:
        return {
            "recommended": None,
            "reason": "No GPU large enough for requirements",
        }
    
    # Sort by cost (cheapest first)
    suitable_gpus.sort(key=lambda x: x["info"]["cost_per_hour"])
    
    # Recommend cheapest that fits
    recommended = suitable_gpus[0]
    
    savings = None
    if current_gpu and current_gpu in GPU_PRICING:
        current_cost = GPU_PRICING[current_gpu]["cost_per_hour"]
        recommended_cost = recommended["info"]["cost_per_hour"]
        savings = {
            "hourly": current_cost - recommended_cost,
            "monthly": calculate_monthly_cost(current_cost - recommended_cost),
            "yearly": calculate_yearly_cost(current_cost - recommended_cost),
        }
    
    return {
        "recommended": recommended["gpu_id"],
        "info": recommended["info"],
        "savings": savings,
        "all_options": suitable_gpus,
    }

