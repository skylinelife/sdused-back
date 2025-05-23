from fastapi import HTTPException, UploadFile
from fastapi import Response
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo
from ser.article_management import createArticleType


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


