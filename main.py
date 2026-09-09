from pathlib import Path
import markdown
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from methods import liste_article,lire_article,create_article,edit_article,liste_comment,create_comment

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.get("/list")(liste_article)
app.get("/article/{article_url}")(lire_article)
app.post("/create")(create_article)
app.post("/article/{article_url}/edit")(edit_article)

app.get("/comments")(liste_comment)
app.post("/comments", status_code=201)(create_comment)


