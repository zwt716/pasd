'''
Author: 嘉欣 罗 2592734121@qq.com
Date: 2022-12-22 12:49:07
LastEditors: Please set LastEditors
LastEditTime: 2023-05-10 15:18:04
FilePath: \psad-backend\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
pip install uvicorn
# 推荐启动方式 main指当前文件名字 app指FastAPI实例化后对象名称
uvicorn main:app --host=127.0.0.1 --port=8010 --reload

类似flask 工厂模式创建
# 生产启动命令 去掉热重载 (可用supervisor托管后台运行)

在main.py同文件下下启动
uvicorn main:app --host=127.0.0.1 --port=8010 --workers=4

# 同样可以也可以配合gunicorn多进程启动  main.py同文件下下启动 默认127.0.0.1:8000端口
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8020

"""


# from common import session
# from fastapi import Depends

import time
from fastapi import Depends
from core.server import create_app
from common import session
import socket
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
app = create_app()
host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
port = 8010


async def reset_db_state():
    session.db._state._state.set(session.db.db_state.copy())
    session.db._state.reset()


# 基于BaseHTTPMiddleware的中间件实例，
class CostimeHeaderMiddleware(BaseHTTPMiddleware):

    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        # print('基于BaseHTTPMiddleware的中间件实例请求开始前')
        start_time = time.time()
        responser = await call_next(request)
        process_time = round(time.time() - start_time, 4)
        # 返回接口响应时间
        responser.headers["X-Process-Time"] = f"{process_time} (s)"
        # print('请求开始前我可以处理事情555555555')
        return responser


# app.add_middleware(CostimeHeaderMiddleware)

# 作者：小钟同学
# 链接：https://juejin.cn/post/6971451349141553165
# 来源：稀土掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
def getApiMap():
    apiMap = {}
    if hasattr(route, "methods"):
        print({'path': route.path, 'name': route.name, 'methods': route.methods})
        apiMap[route.path] = route.name
    return apiMap


if __name__ == "__main__":
    import uvicorn

    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})
    #
    asyncio.run(uvicorn.run(
        app='main:app',
        host="127.0.0.1",
        # host=host,
        port=port,
        reload=True,
        # debug=True
    ))

