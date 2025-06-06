from fastapi import APIRouter, Depends, UploadFile, File

from model.user_setting import userSettingModel
from ser.user_setting import userRegisterType, loginType, setPasswordType, updateUserType
from utils import makeResponse

router = APIRouter(
    prefix="/api/user"
)


# 用户邮箱注册账号
@router.post("/register")
async def register_user(data: userRegisterType):
    db = userSettingModel()
    res = db.registerUser(data)
    return res


# 用户登录
@router.post("/login")
async def login_user(data: loginType):
    db = userSettingModel()
    res = db.loginUser(data)
    return makeResponse(res)


# 用户退出登录
@router.post("/logout")
async def logout_user(user_name: str):
    db = userSettingModel()
    res = db.logoutUser(user_name)
    return makeResponse(res)


# 修改用户密码
@router.post("/set-password")
async def set_password(data: setPasswordType):
    db = userSettingModel()
    res = db.setPassword(data)
    return makeResponse(res)


# 获取当前用户信息
@router.get("/info")
async def get_user_info(user_name: str):
    db = userSettingModel()
    res = db.getUserInfo(user_name)
    return res


# 更新用户信息
@router.post("/update")
async def update_user_info(data: updateUserType):
    db = userSettingModel()
    res = db.updateUserInfo(data)
    return makeResponse(res)


# 统计用户信息，包括totalUsers, 每日每周每月的activeUsers
@router.get("/state")
async def get_user_state():
    db = userSettingModel()
    res = db.getUserState()
    return makeResponse(res)
