from fastapi import APIRouter, Depends, UploadFile, File

from model.admin import adminModel
from ser.admin import adminType
from utils import makeResponse

router = APIRouter(
    prefix="/admin"
)


@router.get("/user/list")
async def get_user_list(admin_name: adminType):
    db = adminModel()
    res = db.getAllUsersInfo(admin_name)
    return res


# @router.post("/article/delete/{id}")
# async def delete_article(aid: int):
#     db = adminModel()
#     db.deleteArticle(aid)
#     return makeResponse(None)
