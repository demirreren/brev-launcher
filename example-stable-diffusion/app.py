"""Simple Stable Diffusion demo with Gradio UI."""

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline
import os

# Check for GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Running on: {device}")

if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Initialize the model (using smaller model for faster loading)
MODEL_ID = "runwayml/stable-diffusion-v1-5"
print(f"📥 Loading model: {MODEL_ID}")

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None,  # Disable for demo purposes
)
pipe = pipe.to(device)

if device == "cuda":
    # Enable memory optimizations
    pipe.enable_attention_slicing()
    
print("✅ Model loaded successfully!")


def generate_image(prompt, negative_prompt, num_steps, guidance_scale):
    """Generate an image from a text prompt."""
    try:
        print(f"🎨 Generating: {prompt}")
        
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_steps,
            guidance_scale=guidance_scale,
        ).images[0]
        
        print("✅ Image generated!")
        return image
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise gr.Error(f"Generation failed: {e}")


# Create Gradio interface
with gr.Blocks(title="🎨 Stable Diffusion on Brev") as demo:
    gr.Markdown("""
    # 🎨 Stable Diffusion Demo
    ### Powered by Brev GPU Cloud
    
    Generate images from text prompts using Stable Diffusion v1.5.
    """)
    
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="A serene landscape with mountains and a lake at sunset...",
                lines=3,
                value="A cute corgi wearing sunglasses on a beach, digital art"
            )
            
            negative_prompt = gr.Textbox(
                label="Negative Prompt (optional)",
                placeholder="blurry, low quality, distorted...",
                lines=2,
                value="blurry, low quality, distorted"
            )
            
            with gr.Row():
                num_steps = gr.Slider(
                    minimum=10,
                    maximum=50,
                    value=25,
                    step=1,
                    label="Inference Steps"
                )
                
                guidance_scale = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=7.5,
                    step=0.5,
                    label="Guidance Scale"
                )
            
            generate_btn = gr.Button("🎨 Generate Image", variant="primary", size="lg")
        
        with gr.Column():
            output_image = gr.Image(label="Generated Image", type="pil")
    
    # Examples
    gr.Examples(
        examples=[
            ["A majestic lion in a cyberpunk city, neon lights, 4k", "blurry, low quality", 25, 7.5],
            ["An astronaut riding a horse on Mars, photorealistic", "cartoon, painting", 30, 8.0],
            ["A cozy coffee shop interior, warm lighting, plants", "dark, messy", 25, 7.0],
            ["A dragon flying over a medieval castle, fantasy art", "blurry, modern", 30, 7.5],
        ],
        inputs=[prompt, negative_prompt, num_steps, guidance_scale],
    )
    
    # Device info
    gr.Markdown(f"""
    ---
    **Device:** {device.upper()} {'✅' if device == 'cuda' else '⚠️'}
    {f"**GPU:** {torch.cuda.get_device_name(0)}" if device == 'cuda' else "**Note:** Running on CPU (slow)"}
    
    💡 **Tip:** Deploy on Brev to get instant GPU access!
    """)
    
    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, negative_prompt, num_steps, guidance_scale],
        outputs=output_image,
    )

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 7860))
    
    print(f"\n🚀 Starting Gradio app on port {port}")
    print(f"📱 Open: http://localhost:{port}\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
    )

