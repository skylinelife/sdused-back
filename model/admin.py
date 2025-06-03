from fastapi import HTTPException, UploadFile
from fastapi import Response
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo
from ser.admin import adminType


# 管理与权限控制操作类
class adminModel(dbSession):

    # 获取所有用户信息
    def getAllUsersInfo(self):
        # 权限检查由前端来做
        users = self.session.query(UserInfo).all()
        # 转为dict并去除None
        result = [self.deleteNone(user.__dict__) for user in users]
        # 去除SQLAlchemy的内部属性
        for item in result:
            item.pop('_sa_instance_state', None)
        return result

    # 删除对应文章
    def deleteArticle(self, aid: int):
        # 删除对应文章
        query = self.session.query(ArticleInfo).filter(
            ArticleInfo.article_id == aid
        )
        for obj in query:
            self.session.delete(obj)
            self.session.flush()
            self.session.commit()

    # 获取站点运行统计信息
    def getStatistics(self):
        from db import ManageData
        data = self.session.query(ManageData).all()
        result = []
        for item in data:
            dict_item = self.deleteNone(item.__dict__)
            dict_item.pop('_sa_instance_state', None)
            result.append(dict_item)
        return result

