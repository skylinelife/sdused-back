from fastapi import APIRouter, Depends, UploadFile, File

from model.admin import adminModel
from ser.admin import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/admin"
)






