from pydantic import BaseModel, ConfigDict


class BlogBase(BaseModel):
    title: str
    content: str
    published: bool | None = None


class BlogPost(BlogBase):
    author_id: int | None = None


class ShowBlog(BlogBase):
    id: int
    author_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# For nested author display (without circular reference)
class AuthorInBlog(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ShowBlogWithAuthor(BlogBase):
    id: int
    author_id: int | None = None
    author: AuthorInBlog | None = None

    model_config = ConfigDict(from_attributes=True)
