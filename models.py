from database import Base
from sqlalchemy import String, Column, Integer


class Comment(Base):
    __tablename__ = "Comment"
    id = Column(String(255), primary_key=True)
    textFr = Column(String(255))
    textEn = Column(String(255))
    publishedAt = Column(String(255))
    authorId = Column(String(255))
    targetId = Column(String(255))

    def __str__(self):
        return f"<Comment id = {self.id} author = {self.authorId}>"