import schedule
import time
import random
import os
import threading
import win32api
from src import (
    take_screenshot_and_analyze,
    AdvancedTextToSpeech,
    SpeechConfig,
    ImageRenderer,
    WindowMode,
    SpeechState
)

def testingTask():
    try:
        time.sleep(3)
        print("=== ScrapyardNoVa Demo ===\n")
        tts = AdvancedTextToSpeech()
        tts.configure(SpeechConfig(rate=150, volume=0.8))

        print("Taking a screenshot and analyzing...")
        result, joke = take_screenshot_and_analyze("What can you see in this screenshot?", generate_joke=True)

        print(f"\nOpenAI Description:\n{result}\n")
        print(f"\nOpenAI Joke:\n{joke}\n")

        image_renderer = ImageRenderer()
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "src", "Morgan-Freeman-PNG-Photo.png") 
        if not image_renderer.load_image(image_path):
            print("Failed to load image.")
            return
        # TODO MAKE THIS WORK WITH ALL SCREEN SIZES?
        screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        x = random.randint(0, screen_width - image_renderer.width) 
        y = random.randint(0, screen_height - image_renderer.height)
        position = (x, y)

        if not image_renderer.create_window(position=position, mode=WindowMode.NOFRAME):
            print("Failed to create window.")
            return


        print(f"Window created at position: {position} with size: ({image_renderer.width}, {image_renderer.height})")
        
        print("Speaking the joke and showing image...")
        render_thread = threading.Thread(
            target=image_renderer.start_render_loop
        )
        render_thread.daemon = True 
        render_thread.start()

        tts.speak_async(joke)

        while tts.state == SpeechState.SPEAKING:
            time.sleep(0.1)

        time.sleep(0.5)
        
        image_renderer.close_window()
        
        render_thread.join(timeout=0.5)
        
        print(f"Task completed at {time.strftime('%H:%M:%S')}. Next run in 1-2 minutes...")
    except Exception as e:
        print(f"Error in task: {e}")
schedule.every(1).to(2).minutes.do(testingTask)

def main():
    print("ScrapyardNoVa running. Press Ctrl+C to exit.")
    try:
        testingTask()
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()