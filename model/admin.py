from fastapi import HTTPException, UploadFile
from fastapi import Response
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo
from ser.admin import adminType


# 管理与权限控制操作类
class adminModel(dbSession):

    # 判断是否是管理员
    def is_admin(self, user_name):
        user = self.session.query(UserInfo).filter(
            UserInfo.user_name == user_name
        ).first()
        if user and getattr(user, "authority", 0) == 1:
            return True
        return False

    # 获取所有用户信息
    def getAllUsersInfo(self, admin_name: adminType):
        # 以后可以在此添加权限检查
        if self.is_admin(admin_name.admin_name):
            users = self.session.query(UserInfo).all()
            # 转为dict并去除None
            result = [self.deleteNone(user.__dict__) for user in users]
            # 去除SQLAlchemy的内部属性
            for item in result:
                item.pop('_sa_instance_state', None)
            return result
        else:
            return HTTPException(status_code=404, detail="Permission Denial")

    # 删除对应文章
    def deleteArticle(self, aid):
        # 删除对应文章
        query = self.session.query(ArticleInfo).filter(
            ArticleInfo.article_id == aid
        )
        for obj in query:
            self.session.delete(obj)
            self.session.flush()
            self.session.commit()
