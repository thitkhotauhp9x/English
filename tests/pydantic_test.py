from typing import Annotated, List
from pydantic import BaseModel, conlist, Field

class Color(BaseModel):
    colors: Annotated[List[int], Field(min_length=1)]


a = Color.model_validate({
    "colors": []
})
print(a)
