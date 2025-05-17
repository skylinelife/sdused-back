from fastapi import APIRouter, Depends, UploadFile, File

# from model.user_setting import classBindingModel
# from ser.user_setting import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/user"
)