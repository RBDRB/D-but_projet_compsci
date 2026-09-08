from pathlib import Path

import markdown
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

ARTICLES_DIR = Path(__file__).parent.parent / "articles"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Article(BaseModel):
    """Article including its content"""

    name: str = Field(
        description="the name of the article",
        examples=["Alphabet"]
    )
    content: str
    articleUrl: str
    source: str


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "It works!!!"}


@app.get("/list")
def liste_article() -> list[ArticleInfo]:
    articles = []

    for fichier in ARTICLES_DIR.glob("*.md"):
        name = fichier.stem

        # "Mon article" -> "Mon_article"
        article_url = name.replace("_", " ")
        name = name.replace("_"," ")

        article = ArticleInfo(
            name=name,
            articleUrl=article_url
        )

        articles.append(article)

    return articles


@app.get("/article/{article_url}")
def lire_article(article_url: str) -> Article:
    # "Mon_article" -> "Mon article"
    name = article_url.replace(" ", "_")
    filename = name + ".md"
    article_path = ARTICLES_DIR / filename
    name = article_url.replace("_", " ")

    source = article_path.read_text(encoding="utf-8")
    content = markdown.markdown(source)

    article = Article(
        name=name,
        articleUrl=article_url,
        content=content,
        source=source
    )

    return article 