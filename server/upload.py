from fastapi import APIRouter, Depends, UploadFile, File

# from model.upload import classBindingModel
# from ser.upload import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/upload"
)