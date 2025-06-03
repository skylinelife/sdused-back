from fastapi import APIRouter, Depends, UploadFile, File
from model.article_management import articleManagementModel
from ser.article_management import createArticleType, updateArticleType, getArticleListType
from utils import makeResponse

router = APIRouter(
    prefix="/api/article"
)


# 发布新文章
@router.post("/create")
async def create_article(data: createArticleType):
    db = articleManagementModel()
    db.createArticle(data)
    return makeResponse(None)


# 修改文章内容
@router.post("/update/{aid}")
async def update_article(aid: int, data: updateArticleType):
    db = articleManagementModel()
    db.updateArticle(aid, data)
    return makeResponse(None)


# 删除文章
@router.post("/delete/{aid}")
async def delete_article(aid: int):
    db = articleManagementModel()
    db.deleteArticle(aid)
    return makeResponse(None)


# 获取文章详情
@router.get("/detail/{aid}")
async def get_article_detail(aid: int):
    db = articleManagementModel()
    res = db.getArticleDetail(aid)
    return res


# 获取文章列表（支持分页）
@router.get("/list")
async def get_article_list(data: getArticleListType = Depends(getArticleListType)):
    db = articleManagementModel()
    res = db.getArticleList(data)
    return res


# 获取当前用户的所有文章
@router.get("/my-articles")
async def get_my_articles(user_name: str):
    db = articleManagementModel()
    res = db.getMyArticles(user_name)
    return res


# 点赞某篇文章
@router.post("/like/{aid}")
async def like_article(aid: int):
    db = articleManagementModel()
    res = db.likeArticle(aid)
    return makeResponse(res)


# 给一个文章取消点赞
@router.post("/unlike/{aid}")
async def unlike_article(aid: int):
    db = articleManagementModel()
    res = db.unlikeArticle(aid)
    return makeResponse(res)


# 返回按点赞数降序排列的文章列表
@router.get("/articleListByLiked")
async def get_article_list_by_liked():
    db = articleManagementModel()
    res = db.getArticleListByLiked()
    return res


# 根据用户名查询文章
@router.get("/searchArticleByUserName")
async def search_article_by_user_name(user_name: str):
    db = articleManagementModel()
    res = db.getArticlesByUserName(user_name)
    return res
