import datetime
from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class userRegisterType(BaseModel):
    # 用户注册
    # sign_in_info 表中信息
    user_name: str
    password: str
    # user_info 表中信息
    email: str
    sex: str = "男"  # 默认性别为男
    icon: Optional[str] = None
    article_num: int = 0
    comment_num: int = 0
    commented_count: int = 0  # 被点赞数
    authority: int = 0  # 默认权限为普通用户


class loginType(BaseModel):
    user_name: str
    password: str


class setPasswordType(BaseModel):
    user_name: str
    password: str


class updateUserType(BaseModel):
    user_name: str
    password: str
    sex: str
    email: str
    icon: Optional[str] = None
