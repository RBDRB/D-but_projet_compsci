from pathlib import Path
import markdown
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "It works!!!"}


@app.get("/list")
def liste_article() -> list:
    articles = []

    for fichier in ARTICLES_DIR.glob("*.md"):
        name = fichier.stem
        article_url = name.replace("_", " ")

        articles.append({
            "name": name,
            "articleUrl": article_url
        })
 
    return articles

@app.get("/article/{article_url}")
def lire_article(article_url):
    name = article_url.replace(" ", "_")
    filename = name + ".md"
    article_path = ARTICLES_DIR / filename
    source = article_path.read_text(encoding="utf-8")
    content = markdown.markdown(source) 

    return {
        "name": name,
        "articleUrl": article_url,
        "content": content,
        "source": content,
    }