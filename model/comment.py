from fastapi import HTTPException, UploadFile
from fastapi import Response
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo, CommentInfo
from ser.comment import createCommentType, replyCommentType, deleteCommentType


# 评论操作类
class commentModel(dbSession):
    # 判断是否是管理员
    def is_admin(self, user_name):
        user = self.session.query(UserInfo).filter(
            UserInfo.user_name == user_name
        ).first()
        if user and getattr(user, "authority", 0) == 1:
            return True
        return False

    # 添加评论
    def addComment(self, data: createCommentType):
        from datetime import datetime
        try:
            new_comment = CommentInfo(
                user_name=data.user_name,
                article_id=data.article_id,
                comment_content=data.comment_content,
                useful_num=0,
                publish_date=datetime.now(),
            )
            self.session.add(new_comment)
            self.session.commit()
            # 更新发布人发布的评论数量
            user = self.session.query(UserInfo).filter(UserInfo.user_name == data.user_name).first()
            if user:
                user.comment_num += 1
                self.session.commit()
            # 更新文章作者收到的评论数量
            author = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == data.article_id).first()
            if author:
                user = self.session.query(UserInfo).filter(UserInfo.user_name == author.user_name).first()
                user.commented_count += 1
                self.session.commit()
            return {"msg": "评论添加成功", "comment_id": new_comment.comment_id}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"评论添加失败: {str(e)}")

    # 获取某篇文章下的所有评论
    def getAllComment(self, aid: int):
        try:
            comments = self.session.query(CommentInfo).filter(CommentInfo.article_id == aid).all()
            result = []
            for item in comments:
                dict_item = self.deleteNone(item.__dict__)
                dict_item.pop('_sa_instance_state', None)
                result.append(dict_item)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取评论失败: {str(e)}")

    # 回复某条评论（效果是对文章进行评论，不是对评论评论）
    def replyComment(self, data: replyCommentType):
        from datetime import datetime
        try:
            new_reply = CommentInfo(
                user_name=data.user_name,
                article_id=data.article_id,
                comment_content=data.comment_content,
                useful_num=0,
                publish_date=datetime.now(),
            )
            self.session.add(new_reply)
            self.session.commit()
            return {"msg": "回复成功", "reply_id": new_reply.comment_id}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"回复失败: {str(e)}")

    # 点赞某条评论
    def likeComment(self, cid: int):
        try:
            comment = self.session.query(CommentInfo).filter(CommentInfo.comment_id == cid).first()
            if not comment:
                raise HTTPException(status_code=404, detail="评论不存在")
            comment.useful_num += 1
            self.session.commit()
            return {"msg": "点赞成功"}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"点赞失败: {str(e)}")

    # 删除某条评论（仅限发布评论者本人或者管理员）
    def deleteComment(self, data: deleteCommentType):
        try:
            comment = self.session.query(CommentInfo).filter(CommentInfo.comment_id == data.comment_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="评论不存在")
            if comment.user_name != data.user_name and not self.is_admin(data.user_name):
                raise HTTPException(status_code=403, detail="没有权限删除该评论")
            self.session.delete(comment)
            self.session.commit()
            # 更新发布人发布的评论数量
            user = self.session.query(UserInfo).filter(UserInfo.user_name == data.user_name).first()
            if user:
                user.comment_num -= 1
                self.session.commit()
            # 更新文章作者收到的评论数量

            author = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == comment.article_id).first()
            if author:
                user = self.session.query(UserInfo).filter(UserInfo.user_name == author.user_name).first()
                user.commented_count -= 1
                self.session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
