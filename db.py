import copy
import json

from sqlalchemy import Column, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, LONGTEXT, \
    FLOAT, BIGINT, TINYINT
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class SignInInfo(Base):
    # 登入信息表
    __tablename__ = 'sign_in_info'

    # 用户名，主键，不允许为空
    user_name = Column(VARCHAR(20), primary_key=True, nullable=False)

    # 账号，主键，不允许为空
    account_number = Column(VARCHAR(20), primary_key=True, nullable=False)

    # 密码，不允许为空
    password = Column(VARCHAR(20), nullable=False)


class UserInfo(Base):
    # 用户信息表
    __tablename__ = 'user_info'

    # 用户名，主键，外键，不允许为空
    user_name = Column(VARCHAR(20), ForeignKey("sign_in_info.user_name"), primary_key=True, nullable=False)

    # 性别，不允许为空
    sex = Column(VARCHAR(10), nullable=False)

    # 邮箱，不允许为空
    email = Column(VARCHAR(20), nullable=False)

    # 头像(存储图片名)
    icon = Column(VARCHAR(20))

    # 文章数量，不允许为空
    article_num = Column(VARCHAR(10), nullable=False)

    # 评论数量，不允许为空
    comment_num = Column(VARCHAR(10), nullable=False)

    # 被评论数量(用作回复提醒)，不允许为空
    commented_count = Column(INTEGER, nullable=False)

    # 用户使用时间(可以没有)
    user_age = Column(DATETIME, nullable=True)

    # 权限，不允许为空
    authority = Column(INTEGER, nullable=False)


class ArticleInfo(Base):
    # 文章信息表
    __tablename__ = 'article_info'

    # 文章id，主键，自增，不允许为空
    article_id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)

    # 用户名，外键，不允许为空
    user_name = Column(VARCHAR(20), ForeignKey("sign_in_info.user_name"), nullable=False)

    # 头像(存储图片名)
    icon = Column(VARCHAR(20))

    # 文章名，唯一，不允许为空
    article_name = Column(VARCHAR(20), nullable=False, unique=True)

    # 图片，存储多个图片路径，可以为空
    picture = Column(VARCHAR(200))

    # 文章内容，不允许为空
    article_content = Column(VARCHAR(1000), nullable=False)

    # 被点赞数量，不为空
    useful_num = Column(INTEGER, nullable=False)

    # 发布日期，不为空
    publish_date = Column(DATETIME, nullable=False)


class CommentInfo(Base):
    # 评论信息表
    __tablename__ = 'comment_info'

    # 评论id，主键，自增，不允许为空
    comment_id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)

    # 用户名，外键，不允许为空
    user_name = Column(VARCHAR(20), ForeignKey("sign_in_info.user_name"), nullable=False)

    # 头像(存储图片名)
    icon = Column(VARCHAR(20))

    # 评论的文章名，外键，不允许为空
    article_name = Column(VARCHAR(20), ForeignKey("article_info.article_name"), nullable=False)

    # 图片，存储多个图片路径
    picture = Column(VARCHAR(200))

    # 评论内容， 不允许为空
    comment_content = Column(VARCHAR(500), nullable=False)

    # 被点赞数量，不为空
    useful_num = Column(VARCHAR(10), nullable=False)

    # 发布日期，不为空
    publish_date = Column(DATETIME, nullable=False)


class ManageData(Base):
    # 管理数据表
    __tablename__ = 'manage_data'

    # 管理员名，主键
    admin_name = Column(VARCHAR(20), primary_key=True, nullable=False)

    # 用户数，不允许为空
    user_num = Column(VARCHAR(20), nullable=False)

    # 头像数据
    icon_data = Column(VARCHAR(20))

    # 评论数，不允许为空
    comment_num = Column(VARCHAR(20), nullable=False)

    # 文章数，不允许为空
    article_num = Column(VARCHAR(20), nullable=False)

    # 运行日期，不允许为空
    run_date = Column(DATETIME, nullable=False)


from const import Mysql_addr, Mysql_user, Mysql_pass, Mysql_db

link = "mysql+pymysql://{}:{}@{}/{}".format(
    Mysql_user, Mysql_pass, Mysql_addr, Mysql_db)


def init_db():
    engine = create_engine(
        link,
        echo=True,
        pool_pre_ping=True
    )
    Base.metadata.create_all(engine)


class dbSession:
    session = None

    def __init__(self):
        engine = create_engine(
            link,
            encoding="utf-8"
        )
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def getSession(self):
        return self.session

    def jsonDumps(self, data, keys):
        for key in keys:
            if key in data and data[key] is not None:
                data[key] = json.dumps(data[key])
        return data

    def jsonLoads(self, data, keys):
        for key in keys:
            if key in data and data[key] is not None:
                data[key] = json.loads(data[key])
        return data

    # 待处理的查出数据，要转换的时间数据，要删除的数据
    def dealData(self, data, timeKeys=None, popKeys=None):
        from utilsTime import getMsTime
        dict_: dict = copy.deepcopy(data.__dict__)
        dict_.pop("_sa_instance_state")
        if popKeys is not None:
            for key in popKeys:
                if key in dict_:
                    dict_.pop(key)
        if timeKeys is not None:
            for key in timeKeys:
                if key in dict_ and dict_[key] is not None:
                    dict_[key] = getMsTime(dict_[key])
        return dict_

    def dealDataToy(self, data, timeKeys=None, saveKeys=None):
        from utilsTime import getMsTime
        dict_: dict = copy.deepcopy(data.__dict__)
        dict_.pop("_sa_instance_state")
        if saveKeys is not None:
            ls = []
            for key in dict_:
                if key not in saveKeys:
                    ls.append(key)
            for x in ls:
                dict_.pop(x)
        if timeKeys is not None:
            for key in timeKeys:
                if key in dict_ and dict_[key] is not None:
                    dict_[key] = getMsTime(dict_[key])
        return dict_

    def deleteNone(self, data):
        if type(data) == list:
            for i in range(len(data)):
                data[i] = self.deleteNone(data[i])
        elif type(data) == dict:
            data = {key: value for key, value in data.items() if
                    value is not None}

        return data

    def dealDataList(self, data, timeKeys=None, popKeys=None):
        dicts = []
        for d in data:
            dicts.append(self.dealData(d, timeKeys, popKeys))
        return dicts

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    init_db()
