from app.schemas.blog import BlogPost

BLOG_DATA = [
    {
        "id": 1,
        "title": "First Blog Post",
        "content": "This is the content of the first blog post.",
        "published": True,
    },
    {
        "id": 2,
        "title": "Second Blog Post",
        "content": "This is the content of the second blog post.",
        "published": False,
    },
    {
        "id": 3,
        "title": "Third Blog Post",
        "content": "This is the content of the third blog post.",
        "published": True,
    },
    {
        "id": 4,
        "title": "Fourth Blog Post",
        "content": "This is the content of the fourth blog post.",
        "published": False,
    }
]

def create_blog(blog_data: BlogPost):
    new_blog = blog_data.model_dump()
    new_blog["id"] = len(BLOG_DATA) + 1
    BLOG_DATA.append(new_blog)
    return BlogPost(**new_blog)


def get_all_blogs():
    return [BlogPost(**blog) for blog in BLOG_DATA]


def get_blog_by_id(blog_id: int):
    blog = next((blog for blog in BLOG_DATA if blog["id"] == blog_id), None)
    return BlogPost(**blog) if blog else None


def update_blog(blog_id: int, blog_data: BlogPost):
    for index, blog in enumerate(BLOG_DATA):
        if blog["id"] == blog_id:
            BLOG_DATA[index].update(blog_data.dict())
            return BlogPost(**BLOG_DATA[index])
    return None


def delete_blog(blog_id: int):
    for index, blog in enumerate(BLOG_DATA):
        if blog["id"] == blog_id:
            return BlogPost(**BLOG_DATA.pop(index))
    return None
