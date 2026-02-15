from app.schemas.blog import BlogPost
from sqlalchemy.orm import Session


def create_blog(blog_data: BlogPost, db: Session):
    new_blog = BlogPost(title=blog_data.title, content=blog_data.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all_blogs(db: Session):
    return db.query(BlogPost).all()


def get_blog_by_id(blog_id: int, db: Session):
    return db.query(BlogPost).filter(BlogPost.id == blog_id).first()


def update_blog(blog_id: int, blog_data: BlogPost, db: Session):
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if blog:
        blog.title = blog_data.title
        blog.content = blog_data.content
        db.commit()
        db.refresh(blog)
        return blog
    return None


def delete_blog(blog_id: int, db: Session):
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if blog:
        db.delete(blog)
        db.commit()
