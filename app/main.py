from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post, user, auth,vote
from fastapi.middleware.cors import CORSMiddleware
#we are using pydantic to do schema validation

#models.Base.metadata.create_all(bind=engine)
# it tells to create the models if they are not created
app = FastAPI() #fast api instance is app
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/") #endpoint , decorator is identified by @
def root():
    return {"message": "Welcome to FastAPI!!!"}









