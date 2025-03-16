import schedule
import time
import os
from src import (
    take_screenshot_and_analyze, 
    AdvancedTextToSpeech,
    SpeechConfig,
    clear_console,
    ImageRenderer
)

def main() -> None:
    """Main function to demonstrate the ImageRenderer."""
    clear_console()
    
    renderer = ImageRenderer()
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, "Morgan-Freeman-PNG-Photo.png")
    
    renderer.render_image(image_path)
    
    # Take a screenshot and analyze it
    print("Taking a screenshot and analyzing...")
    result, joke = take_screenshot_and_analyze("What can you see in this screenshot?", generate_joke=True)
    
    print(f"\nOpenAI Description:\n{result}\n")
    print(f"\nOpenAI Joke:\n{joke}\n")
    
    print("Speaking the joke...")
    tts.speak_async(joke)
    schedule.every(5).minutes.do(testingTask)
def testingTask():
    time.sleep(0)
    print("=== ScrapyardNoVa Demo ===\n")
    tts = AdvancedTextToSpeech()
    tts.configure(SpeechConfig(rate=150, volume=0.8))
    print("Taking a screenshot and analyzing...")
    result, joke = take_screenshot_and_analyze("What can you see in this screenshot?", generate_joke=True)
    print(f"\nOpenAI Description:\n{result}\n")
    print(f"\nOpenAI Joke:\n{joke}\n")
    print("Speaking the joke...")
    tts.speak_async(joke)
    schedule.every(1).minutes.do(testingTask)
    input()
testingTask()

