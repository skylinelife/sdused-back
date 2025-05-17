from datetime import datetime
from starlette.responses import JSONResponse
from utilsTime import getMsTime


def removeNone(d: dict):
    ls = []
    for x in d:
        if d[x] is None:
            ls.append(x)
    for x in ls:
        d.pop(x)


def makeResponse(data):
    response = JSONResponse({
        "code": 0,
        "message": "OK",
        "data": data,
        "timestamp": getMsTime(datetime.now())
    }, status_code=200)
    return response
