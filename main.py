from datetime import datetime
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from utilities import translator, id_creator, send_herokuapp
import models

app = FastAPI()


class NewComment(BaseModel):
    comment: str


class Comment(BaseModel):  # serializer for Comment
    id: str
    textFr: str
    textEn: str
    publishedAt: str
    authorId: str
    targetId: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/target/{target_id}/comments",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED
)
def create_new_comment(target_id: str, comment: NewComment, db: Session = Depends(get_db)):
    comment = comment.comment
    # detect the language of the text
    lang = translator.detect_language(comment)
    if not lang or lang not in {"en", "fr"}:
        raise HTTPException(status_code=400, detail="comment is empty or not in en-fr")
    # translate the comment to the other language (if fr -> en // if en -> fr)
    comment_translate = translator.translate(comment, lang)
    # return texts in english and in french
    text_en, text_fr = translator.return_good_text(comment, comment_translate, lang)
    # create the date in timestamp format
    date = round(datetime.timestamp(datetime.now()))
    # generate an author_id for Comment Model and to send to herokuapp
    author_id = id_creator.create_id_unique("User-")
    # date = datetime.timestamp(now)
    new_comment = models.Comment(
        id=id_creator.create_id_unique("Comment-"),
        textFr=text_fr,
        textEn=text_en,
        publishedAt=date,
        authorId=author_id,
        targetId=target_id
    )
    # send comment and author to herokuapp
    send_herokuapp.send_message_to_herokuapp(comment, author_id)

    # Save new comment in db
    db.add(new_comment)
    db.commit()

    return new_comment


@app.get("/target/{target_id}/comments",
         response_model=List[Comment],
         status_code=status.HTTP_200_OK)
def get_all_comment_of_a_target(target_id: str, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.targetId == target_id).all()
    return comments
