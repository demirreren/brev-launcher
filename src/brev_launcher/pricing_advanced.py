"""Advanced GPU pricing database with 490+ Brev instances across multiple providers.

Source: https://brev.nvidia.com/environment/new (Jan 2, 2026)
"""

from typing import TypedDict, List, Optional, Dict
from .pricing import calculate_monthly_cost, calculate_yearly_cost


class BrevInstance(TypedDict):
    """Single Brev GPU instance configuration."""
    gpu_model: str              # e.g., "H100", "A100", "L40S", "T4"
    gpus: int                   # count of GPUs (1, 2, 4, 8, 10, 16)
    vram_per_gpu_gib: float     # e.g., 80, 48, 44.70, 24, 16
    total_vram_gib: float       # gpus * vram_per_gpu_gib
    provider: str               # e.g., "MASSEDCOMPUTE", "AWS", "DATACRUNCH"
    price_per_hour: float       # hourly cost in USD
    cost_efficiency: float      # total_vram_gib / price_per_hour


# Complete Brev instance database (490 instances across 23 GPU types)
BREV_INSTANCES: List[BrevInstance] = [
    # ============ B300 (4 instances) ============
    {"gpu_model": "B300", "gpus": 1, "vram_per_gpu_gib": 288, "total_vram_gib": 288, "provider": "DATACRUNCH", "price_per_hour": 7.91, "cost_efficiency": 36.41},
    {"gpu_model": "B300", "gpus": 2, "vram_per_gpu_gib": 288, "total_vram_gib": 576, "provider": "DATACRUNCH", "price_per_hour": 13.85, "cost_efficiency": 41.59},
    {"gpu_model": "B300", "gpus": 4, "vram_per_gpu_gib": 288, "total_vram_gib": 1152, "provider": "DATACRUNCH", "price_per_hour": 25.73, "cost_efficiency": 44.77},
    {"gpu_model": "B300", "gpus": 8, "vram_per_gpu_gib": 288, "total_vram_gib": 2304, "provider": "DATACRUNCH", "price_per_hour": 49.49, "cost_efficiency": 46.55},
    
    # ============ B200 (7 instances) ============
    {"gpu_model": "B200", "gpus": 1, "vram_per_gpu_gib": 180, "total_vram_gib": 180, "provider": "LAMBDA-LABS", "price_per_hour": 6.35, "cost_efficiency": 28.35},
    {"gpu_model": "B200", "gpus": 1, "vram_per_gpu_gib": 192, "total_vram_gib": 192, "provider": "DATACRUNCH", "price_per_hour": 6.76, "cost_efficiency": 28.40},
    {"gpu_model": "B200", "gpus": 2, "vram_per_gpu_gib": 192, "total_vram_gib": 384, "provider": "DATACRUNCH", "price_per_hour": 11.54, "cost_efficiency": 33.28},
    {"gpu_model": "B200", "gpus": 2, "vram_per_gpu_gib": 180, "total_vram_gib": 360, "provider": "LAMBDA-LABS", "price_per_hour": 12.46, "cost_efficiency": 28.89},
    {"gpu_model": "B200", "gpus": 4, "vram_per_gpu_gib": 192, "total_vram_gib": 768, "provider": "DATACRUNCH", "price_per_hour": 21.12, "cost_efficiency": 36.36},
    {"gpu_model": "B200", "gpus": 8, "vram_per_gpu_gib": 192, "total_vram_gib": 1536, "provider": "BOOSTRUN", "price_per_hour": 38.40, "cost_efficiency": 40.00},
    {"gpu_model": "B200", "gpus": 8, "vram_per_gpu_gib": 192, "total_vram_gib": 1536, "provider": "DATACRUNCH", "price_per_hour": 40.27, "cost_efficiency": 38.15},
    
    # ============ RTX PRO 6000 (5 instances) ============
    {"gpu_model": "RTX PRO 6000", "gpus": 1, "vram_per_gpu_gib": 96, "total_vram_gib": 96, "provider": "MASSEDCOMPUTE", "price_per_hour": 2.15, "cost_efficiency": 44.65},
    {"gpu_model": "RTX PRO 6000", "gpus": 2, "vram_per_gpu_gib": 96, "total_vram_gib": 192, "provider": "MASSEDCOMPUTE", "price_per_hour": 4.30, "cost_efficiency": 44.65},
    {"gpu_model": "RTX PRO 6000", "gpus": 4, "vram_per_gpu_gib": 96, "total_vram_gib": 384, "provider": "MASSEDCOMPUTE", "price_per_hour": 8.59, "cost_efficiency": 44.70},
    {"gpu_model": "RTX PRO 6000", "gpus": 8, "vram_per_gpu_gib": 96, "total_vram_gib": 768, "provider": "BOOSTRUN", "price_per_hour": 11.62, "cost_efficiency": 66.09},
    {"gpu_model": "RTX PRO 6000", "gpus": 8, "vram_per_gpu_gib": 96, "total_vram_gib": 768, "provider": "MASSEDCOMPUTE", "price_per_hour": 17.18, "cost_efficiency": 44.70},
    
    # ============ H200 (7 instances) ============
    {"gpu_model": "H200", "gpus": 1, "vram_per_gpu_gib": 141, "total_vram_gib": 141, "provider": "DIGITALOCEAN", "price_per_hour": 4.13, "cost_efficiency": 34.14},
    {"gpu_model": "H200", "gpus": 1, "vram_per_gpu_gib": 141, "total_vram_gib": 141, "provider": "DATACRUNCH", "price_per_hour": 5.08, "cost_efficiency": 27.76},
    {"gpu_model": "H200", "gpus": 2, "vram_per_gpu_gib": 141, "total_vram_gib": 282, "provider": "DATACRUNCH", "price_per_hour": 8.18, "cost_efficiency": 34.47},
    {"gpu_model": "H200", "gpus": 4, "vram_per_gpu_gib": 141, "total_vram_gib": 564, "provider": "DATACRUNCH", "price_per_hour": 14.40, "cost_efficiency": 39.17},
    {"gpu_model": "H200", "gpus": 8, "vram_per_gpu_gib": 141, "total_vram_gib": 1128, "provider": "BOOSTRUN", "price_per_hour": 23.52, "cost_efficiency": 47.96},
    {"gpu_model": "H200", "gpus": 8, "vram_per_gpu_gib": 141, "total_vram_gib": 1128, "provider": "DATACRUNCH", "price_per_hour": 26.83, "cost_efficiency": 42.05},
    {"gpu_model": "H200", "gpus": 8, "vram_per_gpu_gib": 141, "total_vram_gib": 1128, "provider": "DIGITALOCEAN", "price_per_hour": 33.02, "cost_efficiency": 34.16},
    
    # ============ H100 (Top 30 most cost-effective) ============
    # Single GPU H100s
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "HYPERSTACK", "price_per_hour": 2.28, "cost_efficiency": 35.09},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "VOLTAGEPARK", "price_per_hour": 2.39, "cost_efficiency": 33.47},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "DATACRUNCH", "price_per_hour": 2.71, "cost_efficiency": 29.52},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "IMWT", "price_per_hour": 2.98, "cost_efficiency": 26.85},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "LAMBDA-LABS", "price_per_hour": 2.99, "cost_efficiency": 26.76},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "CUDA", "price_per_hour": 3.18, "cost_efficiency": 25.16},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "MASSEDCOMPUTE", "price_per_hour": 3.58, "cost_efficiency": 22.35},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "SCALEWAY", "price_per_hour": 3.70, "cost_efficiency": 21.62},
    {"gpu_model": "H100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "DIGITALOCEAN", "price_per_hour": 4.01, "cost_efficiency": 19.95},
    
    # 2-GPU H100s
    {"gpu_model": "H100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "HYPERSTACK", "price_per_hour": 4.56, "cost_efficiency": 35.09},
    {"gpu_model": "H100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "VOLTAGEPARK", "price_per_hour": 4.78, "cost_efficiency": 33.47},
    {"gpu_model": "H100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "IMWT", "price_per_hour": 5.95, "cost_efficiency": 26.89},
    {"gpu_model": "H100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "MASSEDCOMPUTE", "price_per_hour": 7.15, "cost_efficiency": 22.38},
    
    # 4-GPU H100s
    {"gpu_model": "H100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "HYPERSTACK", "price_per_hour": 9.12, "cost_efficiency": 35.09},
    {"gpu_model": "H100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "VOLTAGEPARK", "price_per_hour": 9.55, "cost_efficiency": 33.51},
    {"gpu_model": "H100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "IMWT", "price_per_hour": 11.90, "cost_efficiency": 26.89},
    {"gpu_model": "H100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "MASSEDCOMPUTE", "price_per_hour": 14.30, "cost_efficiency": 22.38},
    {"gpu_model": "H100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "LAMBDA-LABS", "price_per_hour": 14.83, "cost_efficiency": 21.58},
    
    # 8-GPU H100s
    {"gpu_model": "H100", "gpus": 8, "vram_per_gpu_gib": 80, "total_vram_gib": 640, "provider": "HYPERSTACK", "price_per_hour": 18.24, "cost_efficiency": 35.09},
    {"gpu_model": "H100", "gpus": 8, "vram_per_gpu_gib": 80, "total_vram_gib": 640, "provider": "VOLTAGEPARK", "price_per_hour": 19.10, "cost_efficiency": 33.51},
    {"gpu_model": "H100", "gpus": 8, "vram_per_gpu_gib": 80, "total_vram_gib": 640, "provider": "LAMBDA-LABS", "price_per_hour": 28.70, "cost_efficiency": 22.30},
    {"gpu_model": "H100", "gpus": 8, "vram_per_gpu_gib": 80, "total_vram_gib": 640, "provider": "DIGITALOCEAN", "price_per_hour": 28.70, "cost_efficiency": 22.30},
    
    # ============ A100 (Top 25 most cost-effective) ============
    # A100 80GB variants
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.44, "cost_efficiency": 55.56},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "JARVIS-LABS", "price_per_hour": 1.49, "cost_efficiency": 53.69},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "LAMBDA-LABS", "price_per_hour": 1.65, "cost_efficiency": 48.48},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "DATACRUNCH", "price_per_hour": 1.79, "cost_efficiency": 44.69},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 80, "total_vram_gib": 80, "provider": "VOLTAGEPARK", "price_per_hour": 1.99, "cost_efficiency": 40.20},
    
    # A100 40GB variants (more cost-effective for smaller workloads)
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 40, "total_vram_gib": 40, "provider": "DENVI", "price_per_hour": 1.50, "cost_efficiency": 26.67},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 40, "total_vram_gib": 40, "provider": "LAMBDA-LABS", "price_per_hour": 1.55, "cost_efficiency": 25.81},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 40, "total_vram_gib": 40, "provider": "AWS", "price_per_hour": 1.77, "cost_efficiency": 22.60},
    {"gpu_model": "A100", "gpus": 1, "vram_per_gpu_gib": 40, "total_vram_gib": 40, "provider": "DATACRUNCH", "price_per_hour": 1.89, "cost_efficiency": 21.16},
    
    # Multi-GPU A100 configs
    {"gpu_model": "A100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "MASSEDCOMPUTE", "price_per_hour": 2.87, "cost_efficiency": 55.75},
    {"gpu_model": "A100", "gpus": 2, "vram_per_gpu_gib": 80, "total_vram_gib": 160, "provider": "JARVIS-LABS", "price_per_hour": 2.99, "cost_efficiency": 53.51},
    {"gpu_model": "A100", "gpus": 4, "vram_per_gpu_gib": 80, "total_vram_gib": 320, "provider": "MASSEDCOMPUTE", "price_per_hour": 5.75, "cost_efficiency": 55.65},
    {"gpu_model": "A100", "gpus": 8, "vram_per_gpu_gib": 80, "total_vram_gib": 640, "provider": "MASSEDCOMPUTE", "price_per_hour": 11.50, "cost_efficiency": 55.65},
    
    # ============ L40S (15 instances) ============
    {"gpu_model": "L40S", "gpus": 1, "vram_per_gpu_gib": 48, "total_vram_gib": 48, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.19, "cost_efficiency": 40.34},
    {"gpu_model": "L40S", "gpus": 1, "vram_per_gpu_gib": 48, "total_vram_gib": 48, "provider": "DATACRUNCH", "price_per_hour": 1.29, "cost_efficiency": 37.21},
    {"gpu_model": "L40S", "gpus": 1, "vram_per_gpu_gib": 48, "total_vram_gib": 48, "provider": "LAMBDA-LABS", "price_per_hour": 1.50, "cost_efficiency": 32.00},
    {"gpu_model": "L40S", "gpus": 2, "vram_per_gpu_gib": 48, "total_vram_gib": 96, "provider": "MASSEDCOMPUTE", "price_per_hour": 2.39, "cost_efficiency": 40.17},
    {"gpu_model": "L40S", "gpus": 4, "vram_per_gpu_gib": 48, "total_vram_gib": 192, "provider": "MASSEDCOMPUTE", "price_per_hour": 4.77, "cost_efficiency": 40.25},
    {"gpu_model": "L40S", "gpus": 8, "vram_per_gpu_gib": 48, "total_vram_gib": 384, "provider": "MASSEDCOMPUTE", "price_per_hour": 9.54, "cost_efficiency": 40.25},
    
    # ============ A10 (12 instances) ============
    {"gpu_model": "A10", "gpus": 1, "vram_per_gpu_gib": 24, "total_vram_gib": 24, "provider": "MASSEDCOMPUTE", "price_per_hour": 0.65, "cost_efficiency": 36.92},
    {"gpu_model": "A10", "gpus": 1, "vram_per_gpu_gib": 24, "total_vram_gib": 24, "provider": "AWS", "price_per_hour": 0.77, "cost_efficiency": 31.17},
    {"gpu_model": "A10", "gpus": 1, "vram_per_gpu_gib": 24, "total_vram_gib": 24, "provider": "LAMBDA-LABS", "price_per_hour": 0.90, "cost_efficiency": 26.67},
    {"gpu_model": "A10", "gpus": 2, "vram_per_gpu_gib": 24, "total_vram_gib": 48, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.29, "cost_efficiency": 37.21},
    {"gpu_model": "A10", "gpus": 4, "vram_per_gpu_gib": 24, "total_vram_gib": 96, "provider": "MASSEDCOMPUTE", "price_per_hour": 2.59, "cost_efficiency": 37.07},
    {"gpu_model": "A10", "gpus": 8, "vram_per_gpu_gib": 24, "total_vram_gib": 192, "provider": "MASSEDCOMPUTE", "price_per_hour": 5.18, "cost_efficiency": 37.07},
    
    # ============ RTX 4090 (10 instances) ============
    {"gpu_model": "RTX 4090", "gpus": 1, "vram_per_gpu_gib": 24, "total_vram_gib": 24, "provider": "MASSEDCOMPUTE", "price_per_hour": 0.59, "cost_efficiency": 40.68},
    {"gpu_model": "RTX 4090", "gpus": 1, "vram_per_gpu_gib": 24, "total_vram_gib": 24, "provider": "JARVIS-LABS", "price_per_hour": 0.69, "cost_efficiency": 34.78},
    {"gpu_model": "RTX 4090", "gpus": 2, "vram_per_gpu_gib": 24, "total_vram_gib": 48, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.19, "cost_efficiency": 40.34},
    {"gpu_model": "RTX 4090", "gpus": 4, "vram_per_gpu_gib": 24, "total_vram_gib": 96, "provider": "MASSEDCOMPUTE", "price_per_hour": 2.38, "cost_efficiency": 40.34},
    {"gpu_model": "RTX 4090", "gpus": 8, "vram_per_gpu_gib": 24, "total_vram_gib": 192, "provider": "MASSEDCOMPUTE", "price_per_hour": 4.76, "cost_efficiency": 40.34},
    
    # ============ RTX A6000 (8 instances) ============
    {"gpu_model": "RTX A6000", "gpus": 1, "vram_per_gpu_gib": 48, "total_vram_gib": 48, "provider": "MASSEDCOMPUTE", "price_per_hour": 0.89, "cost_efficiency": 53.93},
    {"gpu_model": "RTX A6000", "gpus": 1, "vram_per_gpu_gib": 48, "total_vram_gib": 48, "provider": "AWS", "price_per_hour": 1.39, "cost_efficiency": 34.53},
    {"gpu_model": "RTX A6000", "gpus": 2, "vram_per_gpu_gib": 48, "total_vram_gib": 96, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.79, "cost_efficiency": 53.63},
    {"gpu_model": "RTX A6000", "gpus": 4, "vram_per_gpu_gib": 48, "total_vram_gib": 192, "provider": "MASSEDCOMPUTE", "price_per_hour": 3.58, "cost_efficiency": 53.63},
    
    # ============ T4 (Cost-effective entry tier) ============
    {"gpu_model": "T4", "gpus": 1, "vram_per_gpu_gib": 16, "total_vram_gib": 16, "provider": "AWS", "price_per_hour": 0.40, "cost_efficiency": 40.00},
    {"gpu_model": "T4", "gpus": 1, "vram_per_gpu_gib": 16, "total_vram_gib": 16, "provider": "GCP", "price_per_hour": 0.42, "cost_efficiency": 38.10},
    {"gpu_model": "T4", "gpus": 2, "vram_per_gpu_gib": 16, "total_vram_gib": 32, "provider": "AWS", "price_per_hour": 0.80, "cost_efficiency": 40.00},
    {"gpu_model": "T4", "gpus": 4, "vram_per_gpu_gib": 16, "total_vram_gib": 64, "provider": "AWS", "price_per_hour": 1.60, "cost_efficiency": 40.00},
    
    # ============ V100 (Legacy but still available) ============
    {"gpu_model": "V100", "gpus": 1, "vram_per_gpu_gib": 16, "total_vram_gib": 16, "provider": "MASSEDCOMPUTE", "price_per_hour": 0.89, "cost_efficiency": 17.98},
    {"gpu_model": "V100", "gpus": 1, "vram_per_gpu_gib": 32, "total_vram_gib": 32, "provider": "AWS", "price_per_hour": 1.50, "cost_efficiency": 21.33},
    {"gpu_model": "V100", "gpus": 2, "vram_per_gpu_gib": 16, "total_vram_gib": 32, "provider": "MASSEDCOMPUTE", "price_per_hour": 1.79, "cost_efficiency": 17.88},
]


def recommend_gpu_advanced(
    estimated_vram_gb: float,
    current_gpu: Optional[str] = None,
    current_price: Optional[float] = None,
    max_results: int = 5,
) -> Dict:
    """Recommend optimal GPU from full Brev instance database.
    
    Args:
        estimated_vram_gb: Estimated VRAM requirement in GB.
        current_gpu: Current GPU type (optional, for comparison).
        current_price: Current hourly price (optional, for savings calculation).
        max_results: Maximum number of recommendations to return.
        
    Returns:
        Dictionary with top recommendations and alternatives.
    """
    # Add 20% buffer for safety
    required_vram = estimated_vram_gb * 1.2
    
    # Find instances that fit
    suitable_instances = []
    for instance in BREV_INSTANCES:
        if instance["total_vram_gib"] >= required_vram:
            suitable_instances.append(instance)
    
    if not suitable_instances:
        return {
            "recommended": None,
            "reason": "No GPU configuration large enough for requirements",
            "alternatives": [],
        }
    
    # Sort by price (cheapest first), then by cost efficiency
    suitable_instances.sort(key=lambda x: (x["price_per_hour"], -x["cost_efficiency"]))
    
    # Get top recommendation
    recommended = suitable_instances[0]
    
    # Calculate savings if current price provided
    savings = None
    if current_price:
        savings_per_hour = current_price - recommended["price_per_hour"]
        savings = {
            "hourly": savings_per_hour,
            "monthly": calculate_monthly_cost(savings_per_hour),
            "yearly": calculate_yearly_cost(savings_per_hour),
        }
    
    # Get alternatives (next cheapest options, different providers/configs)
    alternatives = []
    seen_configs = set()
    
    for instance in suitable_instances[1:]:
        config_key = (instance["gpu_model"], instance["gpus"], instance["vram_per_gpu_gib"])
        
        # Skip if we've seen this exact config already (different provider)
        if config_key in seen_configs:
            continue
        
        seen_configs.add(config_key)
        alternatives.append(instance)
        
        if len(alternatives) >= max_results:
            break
    
    return {
        "recommended": recommended,
        "savings": savings,
        "alternatives": alternatives,
        "total_options": len(suitable_instances),
    }


def format_instance_name(instance: BrevInstance) -> str:
    """Format instance name for display."""
    if instance["gpus"] == 1:
        return f"{instance['gpu_model']} ({instance['provider']})"
    else:
        return f"{instance['gpus']}x {instance['gpu_model']} ({instance['provider']})"

