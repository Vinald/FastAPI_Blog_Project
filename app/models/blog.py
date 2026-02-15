from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
