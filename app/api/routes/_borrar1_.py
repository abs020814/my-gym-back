from fastapi import APIRouter, Depends, HTTPException
from ..models._borrar1_ import Article, ArticleBase
from ...database import get_db
import aiomysql
from typing import List

router = APIRouter()

def row_to_article(row):
    (id,title,content,extract,authorName,authorEmail, comments ) = row

    comments_list = []
    if comments:
        for comment_id in comments.split(","):
            comments_list.append(int(comment_id))
    else:
        comments_list= None

    return Article(**{
        "id": id,
        "title": title,
        "content": content,
        "extract": extract,
        "authorName": authorName,
        "authorEmail": authorEmail,
        "comments": comments_list,
    })

@router.get("/", response_model=List[Article])
async def get_articles(db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:

        await cursor.execute("SELECT id,title,content,extract,authorName,authorEmail, comments FROM vw_articles")
        data = await cursor.fetchall()

        response = []
        for row in data:
            response.append(row_to_article(row))
        return response
        #return [row_to_article(row) for row in data] 
    
@router.post("/", response_model=Article)
async def create_post(article: ArticleBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("INSERT INTO articles (title,content,extract,author_name,author_email) VALUES (%s,%s,%s,%s,%s)",
                             (article.title, article.content, article.extract, article.authorName, article.authorEmail))
        await db.commit()
        await cursor.execute("SELECT id,title,content,extract,authorName,authorEmail, comments FROM vw_articles WHERE id = LAST_INSERT_ID()")
        result = await cursor.fetchone()
        return row_to_article(result)
        #return [row_to_article(row) for row in data] 
        
@router.get("/{id}", response_model=Article)
async def get_post(id: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT id, title, content, extract, authorName, authorEmail, comments FROM vw_articles WHERE id = %s", (id,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return row_to_article(result)
    
@router.delete("/{id}", response_model=Article)
async def delete_post(id: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT id, title, content, extract, authorName, authorEmail, comments FROM vw_articles WHERE id = %s", (id,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Article not found")
        
        await cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        await db.commit()

        return row_to_article(result)