from fastapi import APIRouter, Depends, UploadFile, File
from model.article_management import articleManagementModel
from ser.article_management import createArticleType
from utils import makeResponse

router = APIRouter(
    prefix="/article"
)


# 发布新文章
@router.post("/create")
async def create_article(data: createArticleType):
    db = articleManagementModel()
    db.createArticle(data)
    return makeResponse(None)
