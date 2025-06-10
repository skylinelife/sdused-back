from fastapi import APIRouter, Depends, UploadFile, File

# from model.get_image import classBindingModel
# from ser.get_image import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/api/image"
)