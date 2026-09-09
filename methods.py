from pathlib import Path
import markdown
from models import ArticleInfo,ArticleCreate,ArticleEdit,Article,Comment,CommentCreate
from fastapi import FastAPI,HTTPException

ARTICLES_DIR = Path(__file__).parent.parent / "articles"

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

def lire_article(article_url: str) -> Article:
    # "Mon_article" -> "Mon article"
    name = article_url.replace(" ", "_")
    filename = name + ".md"
    article_path = ARTICLES_DIR / filename
    if ".." in article_url:
        raise HTTPException(400,"The article does not exist")
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

def create_article(new_article: ArticleCreate):
    name = new_article.name
    if len(name)>50:
        raise HTTPException(400,"the title is too long")
    if len(name)==0:
        raise HTTPException(400,"No title")
    if ".." in name:
        raise HTTPException(400,"name invalid")

    content = new_article.content
    if len(content)>200000:
        raise HTTPException(400,"Title too long")
    
    source = new_article.content
    new_article_file = ARTICLES_DIR /(name+".md")
    try :
        new_article_file.write_text(content,encoding="utf-8")
    except : 
        print("une erreur")
    article_url = name.replace(" ", "_")

    content = markdown.markdown(source)

    article = Article(
        name = name,
        articleUrl= article_url,  
        content=content,
        source=source
    )
    return article

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

comments: list[Comment] = []
next_comment_id = 1

def liste_comment()-> list[Comment]:
    return comments

def create_comment(new_comment: CommentCreate)->Comment:
    global next_comment_id
    comment = Comment(
        id=next_comment_id,
        content=new_comment.content,  
        author=new_comment.author
    )
    comments.append(comment)
    next_comment_id +=1
    return comment


