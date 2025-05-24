from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class createArticleType(BaseModel):
    # 发布文章
    user_name: str
    article_name: str
    article_content: str
    icon: str = None
    picture: str = None


class updateArticleType(BaseModel):
    # 修改文章
    article_name: str
    article_content: str
    icon: str = None
    picture: str = None


class getArticleListType(BaseModel):
    # 获取文章
    pageNow: int = 1
    pageSize: int = 10
