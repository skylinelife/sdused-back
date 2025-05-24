from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class adminType(BaseModel):
    # 记录管理权限信息
    admin_name: str


class articleType(BaseModel):
    # 记录文章信息
    aid: int
