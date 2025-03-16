from openai import OpenAI
from enum import Enum
from dotenv import load_dotenv
import os
import base64

from .screenshot import ScreenshotManager, PathType
# William is cool!
load_dotenv()

class ImageProcessingOpenAIModelTypes(Enum):
    GPT_4_O = "gpt-4o"
    GPT_4_O_MINI = "gpt-4o-mini"

class ImageProcessingInputDetail(Enum):
    LOW = "low"
    HIGH = "high"
    AUTO = "auto"

def load_openai_client():
    """Initialize and return an OpenAI client using the API key from environment variables."""
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def encode_image(image_path):
    """Convert an image file to base64 encoding."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image_with_openai(client, image_path, prompt, model_type=ImageProcessingOpenAIModelTypes.GPT_4_O, detail=ImageProcessingInputDetail.AUTO):
    """Process an image with OpenAI's vision API."""
    base64_image = encode_image(image_path)
    
    completion = client.chat.completions.create(
        model=model_type.value,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": detail.value
                        },
                    },
                ],
            }
        ],
    )
    
    return completion

def generate_joke_from_description(client, description, model_type=ImageProcessingOpenAIModelTypes.GPT_4_O):
    """Generate a joke about the content of a screen based on its description."""
    prompt = f"""The following is a description of what's on a user's screen: 
    
    {description}
    
    Please make a funny joke about what's on this screen. Keep it light and relevant to the content described. But actully make it funny, it can also be about the user who is on this screen. Or roast them, mainly roast them Witch would be prefered. Dont say anything before or after the roast, just say it."""
    
    completion = client.chat.completions.create(
        model=model_type.value,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    
    return completion.choices[0].message.content

def take_screenshot_and_analyze(prompt="Describe this image", 
                              model_type=ImageProcessingOpenAIModelTypes.GPT_4_O,
                              detail=ImageProcessingInputDetail.AUTO,
                              generate_joke=False):
    """Take a screenshot and analyze it with OpenAI. Optionally generate a joke about the content."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    screenshot_manager = ScreenshotManager()
    image_path = screenshot_manager.save_and_get_path("ai_test_screenshot.png")
    
    openai_client = load_openai_client()
    completion = process_image_with_openai(
        openai_client,
        image_path, 
        prompt, 
        model_type=model_type, 
        detail=detail
    )
    
    analysis = completion.choices[0].message.content
    
    if generate_joke:
        joke = generate_joke_from_description(openai_client, analysis, model_type)
        return analysis, joke
    
    return analysis

if __name__ == "__main__":
    result = take_screenshot_and_analyze()
    print(result)