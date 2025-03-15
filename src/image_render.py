import pygame
import sys
import logging
import os
import win32gui
import win32con
import win32api
import ctypes
from enum import Enum
from typing import Optional, Tuple, Union

class WindowMode(Enum):	
    """Window display modes for the image renderer."""
    NORMAL = 0
    NOFRAME = pygame.NOFRAME
    FULLSCREEN = pygame.FULLSCREEN

class ImageRenderer:
    """
    A class for rendering transparent PNG images using pygame.
    
    This class handles loading images, creating transparent windows,
    and managing the rendering loop.
    """
    
    def __init__(self):
        """Initialize the ImageRenderer."""
        self.image = None
        self.screen = None
        self.running = False
        self.width = 0
        self.height = 0
        self._setup_logging()
        pygame.init()
        self._temp_surface = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        
    def _setup_logging(self) -> None:
        """Configure logging for the image renderer."""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        self.logger.info("ImageRenderer initialized")
        
    def load_image(self, image_path: str) -> bool:
        """
        Load an image from the specified path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if image loaded successfully, False otherwise
        """
        try:
            self.logger.info(f"Loading image from: {image_path}")
            
            if not os.path.isfile(image_path):
                self.logger.error(f"Image file does not exist at {image_path}")
                return False
                
            self.image = pygame.image.load(image_path)
            self.width, self.height = self.image.get_size()
            self.image = self.image.convert_alpha()
            
            self.logger.info(f"Image loaded successfully, size: {self.width}x{self.height}")
            return True
            
        except pygame.error as e:
            self.logger.error(f"Failed to load image: {e}")
            return False
    
    def create_window(self, 
                     position: Tuple[int, int] = (0, 0), 
                     title: str = "Transparent Image",
                     mode: WindowMode = WindowMode.NOFRAME) -> bool:
        """
        Create a window for displaying the image.
        
        Args:
            position: Window position as (x, y) coordinates
            title: Window title
            mode: Window display mode
            
        Returns:
            True if window created successfully, False otherwise
        """
        if self.image is None:
            self.logger.error("Cannot create window: No image loaded")
            return False
            
        try:
            x, y = position
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
            
            self.screen = pygame.display.set_mode(
                (self.width, self.height), 
                mode.value
            )
            pygame.display.set_caption(title)
            
            # Set up transparent window
            hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetWindowLong(
                hwnd,
                win32con.GWL_EXSTYLE,
                win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
            )
            
            win32gui.SetLayeredWindowAttributes(
                hwnd, 
                win32api.RGB(0, 0, 0),
                0,
                win32con.LWA_COLORKEY
            )
            
            self.logger.info(f"Window created: {self.width}x{self.height} at position {position}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create window: {e}")
            return False
    
    def start_render_loop(self) -> None:
        """Start the rendering loop to display the image."""
        if self.image is None or self.screen is None:
            self.logger.error("Cannot start render loop: Image or screen not initialized")
            return
            
        self.running = True
        self.logger.info("Starting render loop")
        
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.logger.info("Quit event detected")
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.logger.info("Escape key pressed, exiting")
                            self.running = False
                
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.image, (0, 0))
                pygame.display.update()
                
        except Exception as e:
            self.logger.error(f"Error in render loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources when rendering is complete."""
        pygame.quit()
        self.logger.info("Resources cleaned up")
        
    def render_image(self, image_path: str, position: Tuple[int, int] = (0, 0)) -> None:
        """
        Load an image and render it at the specified position.
        
        This is a convenience method that chains together loading,
        window creation and rendering.
        
        Args:
            image_path: Path to the image file
            position: Window position as (x, y) coordinates
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if not self.load_image(image_path):
            return
            
        if not self.create_window(position):
            return
            
        self.start_render_loop()

def clear_console() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main() -> None:
    """Main function to demonstrate the ImageRenderer."""
    clear_console()
    
    renderer = ImageRenderer()
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, "Morgan-Freeman-PNG-Photo.png")
    
    renderer.render_image(image_path)

if __name__ == "__main__":
    main()