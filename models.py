from pydantic import BaseModel, Field


class Article(BaseModel):
    """Article including its content"""

    name: str = Field(
        description="the name of the article",  
        examples=["Alphabet"]
    )
    content: str
    articleUrl: str
    source: str

    author: str | None=None
    category: str | None = None
    tags: list[str] = []


class ArticleInfo(BaseModel):
    name: str
    articleUrl: str

class ArticleCreate(BaseModel):
    name: str
    content: str

    author: str | None=None
    category: str | None = None
    tags: list[str] = []

class ArticleEdit(BaseModel):
    content : str
    author: str | None=None
    category: str | None = None
    tags: list[str] = []

class CommentCreate(BaseModel):
     content: str = Field(min_length=1)
     author : str | None = None

class Comment(BaseModel):
    id : int
    content: str
    author : str | None = None
