from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    content: str
    published: bool | None = None
    
    
class BlogPost(BlogBase):
    pass
