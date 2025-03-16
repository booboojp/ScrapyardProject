import pyttsx3
from typing import Dict, List, Optional
import threading
import time
import logging
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SpeechConfig:
    """Configuration container for speech parameters."""
    rate: int = 200
    volume: float = 1.0
    voice_id: str = ""
    
class SpeechState(Enum):
    """Enumeration of valid speech states."""
    IDLE = "idle"
    SPEAKING = "speaking"
    PAUSED = "paused"
    ERROR = "error"

class AdvancedTextToSpeech:
    def __init__(self):
        """Initialize with robust error handling and state management."""
        self.engine = pyttsx3.init(driverName=None, debug=False)
        self.config = SpeechConfig()
        self.state = SpeechState.IDLE
        
        self.engine.connect('started-utterance', self._on_speech_start)
        self.engine.connect('finished-utterance', self._on_speech_finish)
        self.engine.connect('error', self._handle_error)
        
        self._state_lock = threading.Lock()
        self._speech_queue: List[str] = []
        self._queue_lock = threading.Lock()
    
    def _on_speech_start(self, name):
        """Handler for speech start events."""
        with self._state_lock:
            self.state = SpeechState.SPEAKING
            logger.info(f"Started speaking: {name}")
    
    def _on_speech_finish(self, name, completed):
        """Handler for speech completion events."""
        with self._state_lock:
            self.state = SpeechState.IDLE
            logger.info(f"Finished speaking: {name}, completed: {completed}")
    
    def _handle_error(self, name, exception):
        """Handler for speech error events."""
        with self._state_lock:
            self.state = SpeechState.ERROR
            logger.error(f"Speech error: {name}, exception: {str(exception)}")

    def configure(self, config: SpeechConfig) -> None:
        """
        Apply speech configuration with validation and atomic updates.
        
        Args:
            config: SpeechConfig instance containing desired settings
            
        Raises:
            ValueError: If configuration parameters are invalid
        """
        if not (0 <= config.rate <= 400):
            raise ValueError(f"Rate must be between 0 and 400, got {config.rate}")
            
        if not (0.0 <= config.volume <= 1.0):
            raise ValueError(f"Volume must be between 0.0 and 1.0, got {config.volume}")
            
        with self._state_lock:
            self.config = config
            self.engine.setProperty('rate', config.rate)
            self.engine.setProperty('volume', config.volume)
            if config.voice_id:
                self.engine.setProperty('voice', config.voice_id)

    def speak_async(self, text: str) -> None:
        """
        Asynchronous speech processing with queue management.
        
        Args:
            text: Text to be spoken
            
        Raises:
            RuntimeError: If speech engine encounters an error
        """
        if not text.strip():
            logger.warning("Empty text provided")
            return
            
        with self._queue_lock:
            self._speech_queue.append(text)
            
        if self.state == SpeechState.IDLE:
            self._process_next_text()

    def _process_next_text(self) -> None:
        """Internal method for processing queued text."""
        with self._queue_lock:
            if not self._speech_queue:
                return
                
            text = self._speech_queue.pop(0)
            
        try:
            with self._state_lock:
                if self.state != SpeechState.IDLE:
                    logger.info(f"Skipping text: {text[:50]}...")
                    return
                    
                self.state = SpeechState.SPEAKING
                self.engine.say(text)
                
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Speech processing failed: {str(e)}")
            self.state = SpeechState.ERROR
        finally:
            with self._state_lock:
                self.state = SpeechState.IDLE
                self._process_next_text()

    def stop(self) -> None:
        """Immediate termination of ongoing speech."""
        with self._state_lock:
            if self.state == SpeechState.SPEAKING:
                self.engine.stop()
                self.state = SpeechState.IDLE

    def get_state(self) -> Dict[str, any]:
        """Retrieve current system state with synchronization."""
        with self._state_lock:
            voices = [{'id': v.id, 'name': v.name, 'languages': v.languages}
                     for v in self.engine.getProperty('voices')]
            
            return {
                'state': self.state.value,
                'config': vars(self.config),
                'queue_length': len(self._speech_queue),
                'available_voices': voices
            }