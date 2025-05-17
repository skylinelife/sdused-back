from fastapi import APIRouter, Depends, UploadFile, File

# from model.article_management import classBindingModel
# from ser.article_management import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/article"
)
