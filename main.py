from pathlib import Path
import markdown
from fastapi import FastAPI,HTTPException
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

class ArticleCreate(BaseModel):
    name: str
    content: str
class ArticleEdit(BaseModel):
    content : str


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
    if ".." in article_url:
        raise HTTPException(404,"The article does not exist")
    if not article_path.exists():
        raise HTTPException(404,"The article does not exist.")

    source = article_path.read_text(encoding="utf-8")
    content = markdown.markdown(source)
    name = article_url.replace("_", " ")

    article = Article(
        name=name,
        articleUrl=article_url,
        content=content,
        source=source
    )

    return article 

@app.post("/create")
def create_article(new_article: ArticleCreate):
    name = new_article.name
    if len(name)>50:
        raise HTTPException(401,"the title is too long")
    if len(name)==0:
        raise HTTPException(401,"No title")
    if ".." in name:
        raise HTTPException(401,"name invalid")

    content = new_article.content
    source = new_article.content
    new_article_file = ARTICLES_DIR /(name+".md")
    new_article_file.write_text(content,encoding="utf-8")
    article_url = name.replace(" ", "_")

    content = markdown.markdown(source)

    article = Article(
        name = name,
        articleUrl= article_url,  
        content=content,
        source=source
    )
    return article

@app.post("/article/{article_url}/edit")
def edit_article(article_url: str,modification: ArticleEdit):
    #récupère le contenu de l'article de article_url
    #edit le contenu de l'instance d'article
    #renvoie l'article modifié 
    name = article_url.replace("_", " ")
    filename = name+".md"
    article_path = ARTICLES_DIR / filename
    if not article_path.exists():
        raise HTTPException(
            status_code=404,
            detail="The article does not exist."
        )
    article_path.write_text(
        modification.content,
        encoding="utf-8"
    )