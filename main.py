import schedule
import time
from src import (
    take_screenshot_and_analyze, 
    AdvancedTextToSpeech,
    SpeechConfig
)
import time
import schedule

def testingTask():
    time.sleep(5)
    print("=== ScrapyardNoVa Demo ===\n")
    tts = AdvancedTextToSpeech()
    tts.configure(SpeechConfig(rate=150, volume=0.8))
    
    # Take a screenshot and analyze it
    print("Taking a screenshot and analyzing...")
    result, joke = take_screenshot_and_analyze("What can you see in this screenshot?", generate_joke=True)
    
    print(f"\nOpenAI Description:\n{result}\n")
    print(f"\nOpenAI Joke:\n{joke}\n")
    
    print("Speaking the joke...")
    tts.speak_async(joke)
    
    print("Press Enter to exit...")
    input()
testingTask()

#schedule.every(5).minutes.do(testingTask)
#def main():
#	while True:
#		schedule.run_pending()
#		time.sleep(1)
