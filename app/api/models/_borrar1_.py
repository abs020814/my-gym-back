from typing import List, Optional
from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    content: str
    extract: str
    authorName: str
    authorEmail: str

class Article(ArticleBase):
    id: int
    comments: Optional[List[int]] = None
    
