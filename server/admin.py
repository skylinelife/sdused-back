from fastapi import APIRouter, Depends, UploadFile, File

from model.admin import adminModel
from ser.admin import adminType
from utils import makeResponse

router = APIRouter(
    prefix="/api/admin"
)


# 获取所有用户信息（含状态）
@router.get("/user/list")
async def get_user_list(admin_name: adminType):
    db = adminModel()
    res = db.getAllUsersInfo(admin_name)
    return res


# 删除文章
@router.post("/article/delete/{aid}")
async def delete_article(aid: int):
    db = adminModel()
    db.deleteArticle(aid)
    return makeResponse(None)


# 获取平台统计数据
@router.get("/statistics")
async def get_statistics():
    db = adminModel()
    res = db.getStatistics()
    return res
