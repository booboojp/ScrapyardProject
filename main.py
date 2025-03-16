import schedule
import time
from src import (
    take_screenshot_and_analyze, 
    AdvancedTextToSpeech,
    SpeechConfig
)

def run_task():
    """This function takes a screenshot, analyzes it, and speaks the response."""
    print("\n=== Running Task: Screenshot Analysis ===\n")
    
    # Set up text-to-speech
    tts = AdvancedTextToSpeech()
    tts.configure(SpeechConfig(rate=150, volume=0.8))
    
    # Take a screenshot and analyze it
    print("Taking a screenshot and analyzing...")
    result = take_screenshot_and_analyze("What can you see in this screenshot?")
    
    # Print the AI response
    print(f"\nOpenAI Response:\n{result}\n")
    
    # Speak the response
    print("Speaking the response...")
    tts.speak_async(result)

# Schedule the task to run **every hour**
schedule.every(1).minutes.do(run_task)

print("Script started! The task will run every hour.")

# Keep the script running
while True:
    schedule.run_pending()  # Check if it's time to run the task
    time.sleep(1)  # Wait for 1 second before checking again

