from PIL import ImageGrab
import os
import logging
import time
from enum import Enum

class PathType(Enum):
    ABSOLUTE = "absolute"
    LOCAL = "local"  


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = time.strftime("%H.%M.%S", ct)
        return f"[{s}]"

    def format(self, record):
        record.asctime = self.formatTime(record, self.datefmt)
        return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.handlers = []
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter('%(asctime)s %(message)s', datefmt='%H.%M.%S'))
logger.addHandler(handler)

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

class ScreenshotManager:
    def __init__(self):
        self.image = None
    
    @Logging
    def take(self) -> ImageGrab.Image:
        """Take a screenshot of all screens and return the image."""
        self.image = ImageGrab.grab(all_screens=True)
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        return self.image
    
    @Logging
    def _ensure_directory(self, file_path: str) -> None:
        """Ensure the directory exists for the given file path."""
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
    
    @Logging
    def save(self, file_path: str) -> None:
        """Take a screenshot and save it to the specified path."""
        self._ensure_directory(file_path)
        if not self.image:
            self.take()
        self.image.save(file_path, format='PNG')
    
    @Logging
    def save_and_get_path(self, file_path: str, path_type: PathType = PathType.ABSOLUTE) -> str:
        """Take a screenshot, save it, and return the path.
        
        Args:
            file_path: Path where to save the screenshot
            path_type: Type of path to return (ABSOLUTE or LOCAL)
            
        Returns:
            Either absolute or relative path based on path_type
        """
        self.save(file_path)
        if path_type == PathType.ABSOLUTE:
            return os.path.abspath(file_path)
        else:
            return os.path.relpath(file_path)
    
    @Logging
    def process(self, file_path: str, return_path: bool = False, path_type: PathType = PathType.ABSOLUTE) -> str or None:
        """Main processing function that can either save a screenshot or save and return path.
        
        Args:
            file_path: Path where to save the screenshot
            return_path: Whether to return the path (True) or None (False)
            path_type: Type of path to return when return_path=True (ABSOLUTE or LOCAL)
        
        Returns:
            The path if return_path is True, otherwise None
        """
        if return_path:
            return self.save_and_get_path(file_path, path_type)
        else:
            self.save(file_path)
            return None