from openai import OpenAI
from enum import Enum
from dotenv import load_dotenv
import os
import base64
from screenshot import ScreenshotManager, PathType

load_dotenv()
class ImageProcessingOpenAIModelTypes(Enum):
    GPT_4_O = "gpt-4o"
    GPT_4_O_MINI = "gpt-4o-mini"
class ImageProcessingInputDetail(Enum):
    LOW = "low"
    HIGH = "high"
    AUTO = "auto"


def loadOpenAIClient():
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def returnEncodedImagePath(imagePath):
    with open(imagePath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def processImageWithOpenAI(client, image_path, prompt, model_type=ImageProcessingOpenAIModelTypes.GPT_4_O, detail=ImageProcessingInputDetail.AUTO):
    base64_image = returnEncodedImagePath(image_path)
    
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


def main():
    os.system(clear_cmd := 'cls' if os.name == 'nt' else 'clear')
    
    screenshot_manager = ScreenshotManager()
    image_path = screenshot_manager.save_and_get_path("ai_test_screenshot.png")
    
    openAIClient = loadOpenAIClient()
    completion = processImageWithOpenAI(
        openAIClient, 
        image_path, 
        "Describe this image", 
        model_type=ImageProcessingOpenAIModelTypes.GPT_4_O, 
        detail=ImageProcessingInputDetail.AUTO
    )
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main()