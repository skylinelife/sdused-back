from fastapi import HTTPException, UploadFile
from fastapi import Response
# from sqlalchemy import and_, func, delete
from starlette.responses import StreamingResponse

from db import dbSession, UserInfo, SignInInfo
from ser.user_setting import userRegisterType, loginType, setPasswordType, updateUserType


# 用户账户设置
class userSettingModel(dbSession):

    # 用户注册
    def registerUser(self, data: userRegisterType):
        # 检查用户名是否已存在
        existing_user = self.session.query(SignInInfo).filter(SignInInfo.user_name == data.user_name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists.")
        from datetime import datetime
        user = UserInfo(
            user_name=data.user_name,
            sex=data.sex,
            email=data.email,
            icon=data.icon,
            article_num=data.article_num,
            comment_num=data.comment_num,
            commented_count=data.commented_count,
            user_age=datetime.now(),
            authority=data.authority
        )
        signin = SignInInfo(
            user_name=data.user_name,
            password=data.password
        )
        self.session.add(user)
        self.session.add(signin)
        self.session.commit()
        return {"message": "User registered successfully."}

    # 删除用户
    def deleteUser(self, user_id: int):
        user = self.session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return {"message": "User deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # 用户登录
    def loginUser(self, data: loginType):
        user = self.session.query(SignInInfo).filter(
            SignInInfo.user_name == data.user_name,
            SignInInfo.password == data.password
        ).first()
        if user:
            from db import UserInfo
            data = self.session.query(UserInfo).filter(UserInfo.user_name == user.user_name).first()
            return \
                {
                    "message": "Login successful",
                    "user_name": data.user_name,
                    "article_num": data.article_num,
                    "comment_num": data.comment_num,
                    "commented_count": data.commented_count,
                    "authority": data.authority,
                    "email": data.email,
                    "icon": data.icon
                }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    # 用户退出登录
    def logoutUser(self, user_name: str):
        # 这里可以添加一些逻辑，比如清除用户会话等
        return {"message": f"{user_name} logged out successfully."}

    # 修改用户密码
    def setPassword(self, data: setPasswordType):
        user = self.session.query(SignInInfo).filter(
            SignInInfo.user_name == data.user_name
        ).first()
        if user:
            user.password = data.password
            self.session.commit()
            return {"message": "Password updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # 获取用户信息
    def getUserInfo(self, user_name: str):
        from db import UserInfo
        user = self.session.query(UserInfo).filter(UserInfo.user_name == user_name).first()
        if user:
            return {
                "message": "Get user info successfully.",
                "user_name": user.user_name,
                "sex": user.sex,
                "email": user.email,
                "icon": user.icon,
                "article_num": user.article_num,
                "comment_num": user.comment_num,
                "commented_count": user.commented_count,
                "user_age": user.user_age,
                "authority": user.authority
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # 更新用户信息
    def updateUserInfo(self, data: updateUserType):
        from datetime import datetime
        user = self.session.query(UserInfo).filter(UserInfo.user_name == data.user_name).first()
        if user:
            u_user = {
                "user_name": data.user_name,
                "sex": data.sex if data.sex else user.sex,
                # 如果email为空，则不更新
                "email": data.email if data.email else user.email,
                "icon": data.icon if data.icon else user.icon,
                "user_age": datetime.now()  # 更新用户使用时间为当前时间
            }
            self.session.query(UserInfo).filter(UserInfo.user_name == data.user_name).update(u_user)
            self.session.commit()
            return \
                {
                    "message": "User updated successfully.",
                    "user_name": data.user_name,
                    "sex": data.sex if data.sex else user.sex,
                    "email": data.email if data.email else user.email,
                    "icon": data.icon if data.icon else user.icon,
                }
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # 获取用户统计信息
    def getUserState(self):
        from db import UserInfo
        from datetime import datetime, timedelta
        total_users = self.session.query(UserInfo).count()
        active_users_today = self.session.query(UserInfo).filter(
            UserInfo.user_age >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        active_users_this_week = self.session.query(UserInfo).filter(
            UserInfo.user_age >= datetime.now() - timedelta(days=datetime.now().weekday())
        ).count()
        active_users_this_month = self.session.query(UserInfo).filter(
            UserInfo.user_age >= datetime.now().replace(day=1)
        ).count()

        return {
            "totalUsers": total_users,
            "activeUsers": {
                "dau": active_users_today,
                "wau": active_users_this_week,
                "mau": active_users_this_month
            }
        }
