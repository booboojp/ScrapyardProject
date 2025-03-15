from src import (
    take_screenshot_and_analyze, 
    ImageProcessingOpenAIModelTypes, 
    ImageProcessingInputDetail
)

def main():
    print("=== ScrapyardNoVa Demo ===\n")
    
    print("Taking a screenshot and analyzing...")
    result = take_screenshot_and_analyze("What can you see in this screenshot?")
    print(f"\nOpenAI Response:\n{result}\n")

if __name__ == "__main__":
    main()