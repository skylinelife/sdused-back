from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class uploadAvatarType(BaseModel):
    # 上传头像
    user_name: str
    icon: Optional[str] = None
