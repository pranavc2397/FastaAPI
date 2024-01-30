
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import String, func
from sqlalchemy.orm import Session
from app import oauth2
from ..database import get_db
from .. import models, utils, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import joinedload
import json
from ..schemas import PostOut
router = APIRouter( prefix = "/posts", tags=["Posts"])

#,response_model=List[schemas.Post] #,response_model=List[schemas.PostOut]
@router.get("/",response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), limit : int =10, skip:int = 0,
              search : Optional[str] = ""):
    # cursor.execute("""  SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    #posts= posts_query.all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                    models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #posts= posts_query.all()
    #json_results = json.dumps(results)
    #serialized_results = [{'post': result[0], 'votes': result[1]} for result in results]
    print(results[0][1])
    serialized_results = [{'post': result[0], 'votes': result[1]} for result in results]

    return serialized_results
    
    

@router.get("/{id}",response_model=schemas.PostOut) 
def get_posts(id: int, response : Response, db: Session = Depends(get_db), response_model=schemas.Post,
              current_user: int = Depends(oauth2.get_current_user)): #automatic validation of id as integer
    # cursor.execute("""  SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id==id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                    models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"post with id: {id} not found")
    #pydantic_post = schemas.Post.model_validate(post)
    serialized_results = {'post': post[0], 'votes': post[1]} 
    return serialized_results

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.post("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # del_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=  f"post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete()
    db.commit()
    return Response(status_code =status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int, post : schemas.CreatePost,  db: Session = Depends(get_db), response_model=schemas.Post, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content,post.published,str(id)))
    # upd_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    curr_post  = post_query.first()
    if not curr_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=  f"post with id: {id} not found")
    if curr_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump())
    db.commit()
    return post.model_dump()
