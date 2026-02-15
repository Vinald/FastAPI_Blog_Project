from pydantic import BaseModel, ConfigDict

class BlogBase(BaseModel):
    title: str
    content: str
    published: bool | None = None
    
    
class BlogShow(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BlogPost(BlogBase):
    pass
