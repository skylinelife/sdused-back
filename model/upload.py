from fastapi import HTTPException, UploadFile
from fastapi import Response
from starlette.responses import StreamingResponse

from db import dbSession, SignInInfo, UserInfo, ArticleInfo, CommentInfo
from ser.upload import uploadAvatarType


# 上传文件类
class uploadModel(dbSession):

    # 上传头像
    def uploadAvatar(self, data: uploadAvatarType):
        # 将传来的icon数据保存到userInfo对应条目中
        user = self.session.query(UserInfo).filter(UserInfo.user_name == data.user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.icon = data.icon
        self.session.commit()
        return {"message": "Avatar uploaded successfully", "icon": data.icon}
