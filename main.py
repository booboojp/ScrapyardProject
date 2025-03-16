from src import (
    take_screenshot_and_analyze, 
    ImageProcessingOpenAIModelTypes, 
    ImageProcessingInputDetail,
    AdvancedTextToSpeech,
    SpeechConfig
)

def main():
    print("=== ScrapyardNoVa Demo ===\n")
    tts = AdvancedTextToSpeech()
    tts.configure(SpeechConfig(rate=150, volume=0.8))
    
    print("Taking a screenshot and analyzing...")
    result = take_screenshot_and_analyze("What can you see in this screenshot?")
    
    print(f"\nOpenAI Response:\n{result}\n")
    
    print("Speaking the response...")
    tts.speak_async(result)
    
    print("Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()