from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    content: str
    published: bool | None = None
    
    
class BlogShow(BlogBase):
    id: int

    class Config:
        orm_mode = True

class BlogPost(BlogBase):
    pass
