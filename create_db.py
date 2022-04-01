from database import Base, engine
from models import Comment

Base.metadata.create_all(engine)
