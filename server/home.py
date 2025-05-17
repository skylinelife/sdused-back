from fastapi import APIRouter, Depends, UploadFile, File

from model.home import classBindingModel
from ser.home import createClassroom, classroomEditType, userSeatListType
from utils import makeResponse

router = APIRouter(
    prefix="/home"
)