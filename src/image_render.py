import pygame
import logging
import os
import win32gui
import win32con
import win32api
import threading
from enum import Enum
from typing import Tuple

class WindowMode(Enum):
    """Window display modes for the image renderer."""
    NORMAL = 0
    NOFRAME = pygame.NOFRAME
    FULLSCREEN = pygame.FULLSCREEN

QUIT_EVENT = pygame.USEREVENT + 1

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
        self.hwnd = None  
        self._lock = threading.Lock()  
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

            self.hwnd = pygame.display.get_wm_info()["window"] 
            

            win32gui.SetWindowLong(
                self.hwnd,
                win32con.GWL_EXSTYLE,
                win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
            )


            win32gui.SetLayeredWindowAttributes(
                self.hwnd,
                win32api.RGB(0, 0, 0),
                0,
                win32con.LWA_COLORKEY
            )
            
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST,
                x, y,
                self.width, self.height,
                win32con.SWP_SHOWWINDOW
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
                    elif event.type == QUIT_EVENT:
                        self.logger.info("Custom quit event received")
                        self.running = False
                        break

                if not self.running:
                    break

                self.screen.fill((0, 0, 0))
                self.screen.blit(self.image, (0, 0))
                pygame.display.update()
                
                pygame.time.wait(10)

        except Exception as e:
            self.logger.error(f"Error in render loop: {e}")
        finally:
            self.cleanup()

    def stop_rendering(self) -> None:
        """
        Signal the render loop to stop and forcibly close all pygame windows.
        This is a more aggressive approach to ensure windows are closed.
        """
        with self._lock:
            self.logger.info("Forcibly stopping all rendering...")
            self.running = False
            self.close_window()

    def cleanup(self) -> None:
        """Clean up resources when rendering is complete."""
        with self._lock:
            if hasattr(pygame, 'quit'):
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

    def close_window(self) -> None:
        """Close the rendering window in a thread-safe way and force pygame cleanup."""
        with self._lock:
            try:
                if self.hwnd:
                    try:
                        win32gui.DestroyWindow(self.hwnd)
                    except Exception as e:
                        self.logger.error(f"Error destroying window: {e}")
                    
                pygame.display.quit()
                pygame.quit()
                
                self.hwnd = None
                self.screen = None
                self.running = False
                
                self.logger.info("Forced window closure and pygame shutdown")
            except Exception as e:
                self.logger.error(f"Error during forced window closure: {e}")

    def set_window_position(self, position: Tuple[int, int]) -> None:
        """Set the position of the rendering window."""
        if self.hwnd:
            x, y = position
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, x, y, 0, 0, win32con.SWP_NOSIZE)
            self.logger.info(f"Window position set to {position}")