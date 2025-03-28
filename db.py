import copy
import json

from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
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

    # 头像(存储图片名)，不允许为空
    icon = Column(VARCHAR(20), nullable=False)

    # 文章数量，不允许为空
    article_num = Column(VARCHAR(10), nullable=False)

    # 评论数量，不允许为空
    comment_num = Column(VARCHAR(10), nullable=False)

    # 被评论数量(用作回复提醒)，不允许为空
    commented_count = Column(INTEGER, nullable=False)

    # 用户使用时间(可以没有)，不允许为空
    user_age = Column(DATETIME, nullable=False)

    # 权限，不允许为空
    authority = Column(INTEGER, nullable=False)


class ArticleInfo(Base):
    # 文章信息表
    __tablename__ = 'article_info'

    # 用户名，主键，外键，不允许为空
    user_name = Column(VARCHAR(20), ForeignKey("sign_in_info.user_name"), primary_key=True, nullable=False)

    # 头像(存储图片名)，不允许为空
    icon = Column(VARCHAR(20), nullable=False)

    # 文章名，不允许为空
    article_name = Column(VARCHAR(20), nullable=False)

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

    # 用户名，主键，外键，不允许为空
    user_name = Column(VARCHAR(20), ForeignKey("sign_in_info.user_name"), primary_key=True, nullable=False)

    # 头像(存储图片名)，不允许为空
    icon = Column(VARCHAR(20), nullable=False)

    # 评论名，不允许为空
    comment_name = Column(VARCHAR(20), nullable=False)

    # 图片，存储多个图片路径，可以为空
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

    # 头像数据，不允许为空
    icon_data = Column(VARCHAR(20), nullable=False)

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


if __name__ == "__main__":
    init_db()
