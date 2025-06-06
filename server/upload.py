from fastapi import APIRouter, Depends, UploadFile, File

from ser.upload import uploadAvatarType
# from model.upload import classBindingModel
# from ser.upload import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/api/upload"
)


# 上传头像
@router.post("/avatar")
async def upload_avatar(data: uploadAvatarType):
    from model.upload import uploadModel
    db = uploadModel()
    res = db.uploadAvatar(data)
    return makeResponse(res)
