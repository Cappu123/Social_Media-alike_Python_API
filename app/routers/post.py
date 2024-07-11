from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.postOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """Retrieves all posts"""

    print(limit)
    #posts = db.query(models.Post).filter(
     #   models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
   
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Creates a post"""

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    return new_post


@router.get("/{id}", response_model=schemas.postOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Retrieves a specific post"""
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,) )
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                         isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(posts)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: 
                int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
     
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (id,)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
   # if post.owner_id != oauth2.get_current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
     #                       detail="Not authorized to perform the requested action")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform the requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


