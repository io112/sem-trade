from typing import Optional, Dict

from pydantic import BaseModel


class SuggestionRequest(BaseModel):
    only_present: Optional[bool]
    part_params: Optional[Dict[str, str]]
    part_type: str

