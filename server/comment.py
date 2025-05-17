from fastapi import APIRouter, Depends, UploadFile, File

from model.comment import classBindingModel
from ser.comment import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/comment"
)

