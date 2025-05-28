import datetime
from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class userRegisterType(BaseModel):
    from datetime import datetime
    # 用户注册
    # sign_in_info 表中信息
    user_name: str
    account_number: str
    password: str
    # user_info 表中信息
    sex: str
    email: str
    icon: Optional[str] = None
    article_num: int = 0
    comment_num: int = 0
    commented_count: int = 0  # 被点赞数
    user_age: datetime = datetime.now()  # 用户使用时间
    authority: int = 0  # 默认权限为普通用户


class loginType(BaseModel):
    account_number: str
    password: str


class setPasswordType(BaseModel):
    account_number: str
    password: str


class updateUserType(BaseModel):
    from datetime import datetime
    user_name: str
    account_number: str
    password: str
    sex: str
    email: str
    icon: Optional[str] = None
    user_age: datetime = datetime.now()  # 用户使用时间
