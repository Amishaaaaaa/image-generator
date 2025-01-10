# import os
# import random
# from PIL import Image, ImageDraw, ImageFont

# def generate_image(params):
#     # Simulated image generation using PIL
#     seed = params.get("seed", random.randint(1, 1e9))
#     width = params.get("width", 512)
#     height = params.get("height", 512)
#     text = params.get("text", "Generated Image")
    
#     # Create image
#     random.seed(seed)
#     image = Image.new("RGB", (width, height), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.load_default()
#     draw.text((10, 10), text, fill="white", font=font)
    
#     # Save image
#     image_path = f"image_{seed}.png"
#     output_dir = os.path.join(os.getcwd(), 'static/generated_images')
#     os.makedirs(output_dir, exist_ok=True)
#     image.save(os.path.join(output_dir, image_path))
#     return image_path


import os
import random
import requests

# Base URL of your ComfyUI API
COMFYUI_API_URL = "http://127.0.0.1:8188/prompt"

def generate_image(params):
    """
    Generates an image using the ComfyUI API and saves it locally.
    :param params: Dictionary containing parameters for the API request.
    :return: Path to the saved image.
    """
    # Define the payload based on the updated API format
    payload = {
        "3": {
            "inputs": {
                "seed": params.get("seed", random.randint(1, 1e9)),
                "steps": params.get("steps", 20),
                "cfg": params.get("cfg", 8),
                "sampler_name": params.get("sampler_name", "euler"),
                "scheduler": params.get("scheduler", "normal"),
                "denoise": params.get("denoise", 1),
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"},
        },
        "4": {
            "inputs": {
                "ckpt_name": params.get("model", "realvisxlV50_v50LightningBakedvae.safetensors"),
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"},
        },
        "5": {
            "inputs": {
                "width": params.get("width", 512),
                "height": params.get("height", 512),
                "batch_size": params.get("batch_size", 1),
            },
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"},
        },
        "6": {
            "inputs": {
                "text": params.get(
                    "positive_prompt",
                    "beautiful scenery nature glass bottle landscape, purple galaxy bottle,"
                ),
                "clip": ["4", 1],
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Prompt)"},
        },
        "7": {
            "inputs": {
                "text": params.get("negative_prompt", "text, watermark"),
                "clip": ["4", 1],
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "CLIP Text Encode (Prompt)"},
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2],
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"},
        },
        "9": {
            "inputs": {
                "filename_prefix": params.get("filename_prefix", "ComfyUI"),
                "images": ["8", 0],
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"},
        },
    }

    # Debugging: Print the payload
    print("Payload being sent to API:", payload)

    # Send the POST request to the ComfyUI API
    try:
        response = requests.post(COMFYUI_API_URL, json=payload)
        response.raise_for_status()  # Raise an error if the request fails
        result = response.json()  # Get the API response as JSON

        # Debugging: Print the API response
        print("Response from API:", result)

        # Extract the filename or image path from the response
        # Assuming the response contains the output path
        output_path = result.get("output", {}).get("images", [])
        if not output_path:
            print("Response does not contain 'images'. Check API response structure.")
            return None


        # Save the generated image to a local directory
        output_dir = os.path.join(os.getcwd(), "static/generated_images")
        os.makedirs(output_dir, exist_ok=True)
        image_path = os.path.join(output_dir, f"{payload['9']['inputs']['filename_prefix']}.png")

        # If the response contains the image content, download and save it
        with open(image_path, "wb") as f:
            f.write(requests.get(output_path[0]).content)

        print(f"Image saved at: {image_path}")
        return image_path

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None



# Example usage
if __name__ == "__main__":
    params = {
        "seed": 868321251806476,
        "steps": 20,
        "cfg": 8,
        "sampler_name": "euler",
        "scheduler": "normal",
        "denoise": 1,
        "width": 512,
        "height": 512,
        "batch_size": 1,
        "model": "realvisxlV50_v50LightningBakedvae.safetensors",
        "positive_prompt": "beautiful scenery nature glass bottle landscape, purple galaxy bottle",
        "negative_prompt": "text, watermark",
        "filename_prefix": "ComfyUI"
    }

    image_path = generate_image(params)
    if image_path:
        print(f"Image successfully generated and saved at: {image_path}")
    else:
        print("Image generation failed.")
