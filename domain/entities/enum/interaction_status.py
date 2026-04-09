
from enum import Enum

class InteractionStatus(Enum):
    SENT = "sent"
    PROCESSING = "processing"
    FINISHED = "finished"
    ERROR = "error"
