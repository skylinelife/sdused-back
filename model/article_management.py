from fastapi import HTTPException, UploadFile
from fastapi import Response
from sqlalchemy import func
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo, CommentInfo
from ser.article_management import createArticleType, updateArticleType, getArticleListType


# 文章管理操作类
class articleManagementModel(dbSession):

    # 发布新文章
    def createArticle(self, data: createArticleType):
        from datetime import datetime
        try:
            new_article = ArticleInfo(
                user_name=data.user_name,
                icon=data.icon,
                article_name=data.article_name,
                picture=data.picture,
                article_content=data.article_content,
                useful_num=0,
                publish_date=datetime.now()
            )
            self.session.add(new_article)
            self.session.commit()
            return {"msg": "文章发布成功", "article_id": new_article.article_id}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"文章发布失败: {str(e)}")

    # 修改文章内容
    def updateArticle(self, aid: int, data: updateArticleType):
        # 可以修改文章名，文章内容
        try:
            article = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == aid).first()
            if not article:
                raise HTTPException(status_code=404, detail="文章不存在")
            article.article_name = data.article_name
            article.article_content = data.article_content
            article.picture = data.picture
            self.session.commit()
            return {"msg": "文章修改成功"}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"文章修改失败: {str(e)}")

    # 删除文章
    def deleteArticle(self, aid: int):
        try:
            article = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == aid).first()
            if not article:
                raise HTTPException(status_code=404, detail="文章不存在")
            # 删除文章前先删除所有该文章下的评论
            from db import CommentInfo
            self.session.query(CommentInfo).filter(CommentInfo.article_id == aid).delete()
            # 删除文章
            self.session.delete(article)
            self.session.commit()
            return {"msg": "文章删除成功"}
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=f"文章删除失败: {str(e)}")

    # 获取文章详情
    def getArticleDetail(self, aid: int):
        try:
            article = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == aid).first()
            if not article:
                raise HTTPException(status_code=404, detail="文章不存在")
            return {
                "user_name": article.user_name,
                "article_name": article.article_name,
                "article_content": article.article_content,
                "icon": article.icon,
                "picture": article.picture,
                "useful_num": article.useful_num,
                "publish_date": article.publish_date
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文章详情失败: {str(e)}")

    # 获取所有文章列表（支持分页）
    def getArticleList(self, data: getArticleListType):
        try:
            articles = self.session.query(ArticleInfo).offset((data.pageNow - 1) * data.pageSize).limit(data.pageSize).all()
            total = self.session.query(ArticleInfo).count()
            return {
                "total": total,
                "articles": [
                    {
                        "article_id": article.article_id,
                        "user_name": article.user_name,
                        "article_name": article.article_name,
                        "icon": article.icon,
                        "picture": article.picture,
                        "useful_num": article.useful_num,
                        "publish_date": article.publish_date
                    } for article in articles
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文章列表失败: {str(e)}")

    # 获取当前用户的所有文章
    def getMyArticles(self, user_name: str):
        try:
            articles = self.session.query(ArticleInfo).filter(ArticleInfo.user_name == user_name).all()
            return [
                {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "icon": article.icon,
                    "picture": article.picture,
                    "useful_num": article.useful_num,
                    "publish_date": article.publish_date
                } for article in articles
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取用户文章失败: {str(e)}")

    # 点赞某篇文章
    def likeArticle(self, aid: int):
        try:
            article = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == aid).first()
            if not article:
                raise HTTPException(status_code=404, detail="文章不存在")
            article.useful_num += 1
            self.session.commit()
            return {"message": "点赞成功"}
        except Exception as e:
            self.session.rollback()
            return {"message": f"点赞失败{str(e)}"}

    # 给一个文章取消点赞
    def unlikeArticle(self, aid: int):
        try:
            article = self.session.query(ArticleInfo).filter(ArticleInfo.article_id == aid).first()
            if not article:
                raise HTTPException(status_code=404, detail="文章不存在")
            if article.useful_num > 0:
                article.useful_num -= 1
                self.session.commit()
                return {"message": "取消点赞成功"}
            else:
                return {"message": "文章点赞数已为0，无需取消点赞"}
        except Exception as e:
            self.session.rollback()
            return {"message": f"取消点赞失败{str(e)}"}

    # 返回按点赞数降序排列的文章列表
    def getArticleListByLiked(self):
        try:
            articles = self.session.query(ArticleInfo).order_by(ArticleInfo.useful_num.desc()).all()
            return [
                {
                    "article_id": article.article_id,
                    "user_name": article.user_name,
                    "article_name": article.article_name,
                    "icon": article.icon,
                    "picture": article.picture,
                    "useful_num": article.useful_num,
                    "publish_date": article.publish_date
                } for article in articles
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取按点赞数排序的文章失败: {str(e)}")

    # 根据用户名查询文章
    def getArticlesByUserName(self, user_name: str):
        try:
            articles = self.session.query(ArticleInfo).filter(ArticleInfo.user_name == user_name).all()
            return [
                {
                    "user_name": article.user_name,
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "article_content": article.article_content,
                    "icon": article.icon,
                    "picture": article.picture,
                    "useful_num": article.useful_num,
                    "publish_date": article.publish_date
                } for article in articles
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"根据用户名查询文章失败: {str(e)}")

    # 统计文章信息，包括总文章数、总评论数、总like数、每日新增文章数
    def getArticleState(self):
        try:
            total_articles = self.session.query(ArticleInfo.article_id).count()
            total_comments = self.session.query(CommentInfo.comment_id).count()  # 假设CommentInfo是评论表
            total_likes = self.session.query(func.sum(ArticleInfo.useful_num)).scalar() or 0
            # 计算每日新增文章数
            from datetime import datetime, timedelta
            today = datetime.now()
            daily_new_articles = self.session.query(ArticleInfo).filter(
                ArticleInfo.publish_date >= today - timedelta(days=1)
            ).count()
            return {
                "totalArticles": total_articles,
                "newArticlesToday": daily_new_articles,
                "totalComments": total_comments,
                "totalLikes": total_likes,  # 文章的总获赞数
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文章统计信息失败: {str(e)}")

    # 返回点赞量最高的5个article的id、title、点赞数
    def getTopArticle(self):
        try:
            top_articles = self.session.query(
                ArticleInfo.article_id,
                ArticleInfo.article_name,
                ArticleInfo.useful_num
            ).order_by(ArticleInfo.useful_num.desc()).limit(5).all()
            return [
                {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "useful_num": article.useful_num
                } for article in top_articles
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取点赞量最高的文章失败: {str(e)}")



