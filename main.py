from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from server import admin, article_management, comment, get_image, home, upload, user_setting
from utilsTime import getMsTime

app = FastAPI()
app.include_router(admin.router)
app.include_router(article_management.router)
app.include_router(comment.router)
app.include_router(user_setting.router)
app.include_router(upload.router)
# app.include_router(get_image.router)
# app.include_router(home.router)


origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源列表
    allow_credentials=True,  # 允许返回 cookies
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)


@app.exception_handler(HTTPException)  # 自定义HttpRequest 请求异常
async def http_exception_handle(request, exc):
    response = JSONResponse({
        "code": exc.status_code,
        "message": str(exc.detail),
        "data": None,
        "timestamp": getMsTime(datetime.now())
    }, status_code=exc.status_code)
    return response


@app.exception_handler(RequestValidationError)
async def request_validation_error(request, exc):
    try:
        message = str(exc.detail)
    except:
        try:
            message = str(exc.raw_errors[0].exc)
        except:
            message = "请求错误"
    response = JSONResponse({
        "code": 400,
        "message": message,
        "data": None,
        "timestamp": getMsTime(datetime.now())
    }, status_code=400)
    return response


@app.exception_handler(Exception)
async def request_validation_error(request, exc):
    if str(exc) == "未登录":
        response = JSONResponse({
            "code": 403,
            "message": "未登录",
            "data": None,
            "timestamp": getMsTime(datetime.now())
        }, status_code=500)
    else:
        response = JSONResponse({
            "code": 500,
            "message": "内部错误",
            "data": None,
            "timestamp": getMsTime(datetime.now())
        }, status_code=500)
    return response


