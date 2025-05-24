from fastapi import APIRouter, Depends, UploadFile, File

from model.comment import commentModel
from ser.comment import createCommentType, replyCommentType, deleteCommentType
from utils import makeResponse

router = APIRouter(
    prefix="/api/comment"
)


# 添加评论
@router.post("/add")
async def add_comment(data: createCommentType):
    db = commentModel()
    res = db.addComment(data)
    return makeResponse(res)


# 获取某篇文章下的所有评论
@router.get("/list/{aid}")
async def get_all_comment(aid: int):
    db = commentModel()
    res = db.getAllComment(aid)
    return res


# 回复某条评论
@router.post("/reply/{cid}")
async def reply_comment(data: replyCommentType):
    db = commentModel()
    res = db.replyComment(data)
    return makeResponse(res)


# 点赞某条评论
@router.post("/like/{cid}")
async def like_comment(cid: int):
    db = commentModel()
    res = db.likeComment(cid)
    return makeResponse(res)


# 删除某条评论  ####
@router.post("/delete")
async def delete_comment(data: deleteCommentType):
    db = commentModel()
    res = db.deleteComment(data)
    return makeResponse(res)

