from typing import List, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session

from db import dbSession


class createCommentType(BaseModel):
    # 发布评论
    user_name: str  # 评论者用户名
    article_id: int  # 被评论文章id
    comment_content: str  # 评论内容


class replyCommentType(BaseModel):
    # 回复评论
    user_name: str  # 评论者用户名
    article_id: int  # 被回复文章的id
    comment_content: str  # 回复内容


class deleteCommentType(BaseModel):
    # 删除评论
    user_name: str  # 操作者用户名(发出删除请求的人)
    comment_id: int  # 被删除评论的id
