from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
from .import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi_crud user=postgres password=1234",
            row_factory=dict_row)

        cursor = conn.cursor()

        print("DB SUccess")

        break
    except Exception as e:
        print("DB connection failed")
        print("Error", e)
        time.sleep(2)

my_posts = [
    {
        "title": "Post Title 1", "content": "Post Content 1", "id": 1
    },
    {
        "title": "Post Title 2", "content": "Post Content 2", "id": 2
    }
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"dats": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createposts(post: Post, db: Session = Depends(get_db)):

    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES \
    #         (%s ,%s, %s) RETURNING * ",
    #     (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/post/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found"
                            )
    return {"post_detail": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()

    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exists")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s \
    #     WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, id,))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exists")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}
