from PIL import ImageGrab
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def Logging(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {str(e)}")
            raise
        finally:
            logger.info(f"{func.__name__} finished execution")
    return wrapper
@Logging
def takeScreenshot() -> ImageGrab.Image:
    img = ImageGrab.grab(all_screens=True)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img
@Logging
def ensureDirectoryExists(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
@Logging
def returnScreenshot(file_path: str) -> None:
    ensureDirectoryExists(file_path)
    img = takeScreenshot()
    img.save(file_path, format='PNG')

@Logging
def main() -> None:
    returnScreenshot("test.png")

if __name__ == "__main__":
    main()