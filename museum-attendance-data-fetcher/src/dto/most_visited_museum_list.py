from dataclasses import dataclass
from typing import List
from .museum import Museum

@dataclass
class MostVisitedMuseumList:
    wikipedia_museum_instance_list: List[Museum]
