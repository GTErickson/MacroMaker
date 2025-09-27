from dataclasses import dataclass
from typing import List
from enum import Enum

class ErrorCategory(Enum):
    FILE = "file"
    FORMAT = "format"
    ROW = "row"
    VALIDATION = "validation"

class ErrorSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"

@dataclass
class LoaderError:
    category: ErrorCategory
    severity: ErrorSeverity
    message: str = ""
    line_number: int = 0
