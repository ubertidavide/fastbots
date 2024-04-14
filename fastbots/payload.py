from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Payload:
    """
    Payload class for managing input data, downloads, and output data.
    """

    input_data: Dict[str, str] = field(default_factory=dict)
    downloads: List[str] = field(default_factory=list)
    output_data: Dict[str, str] = field(default_factory=dict)