<h1>智策后台系统（非国际化版本）</h1>
*by Mr.Robot*

## 介绍

智策极速开发，开箱即用

前端是基于 [vue-pure-admin](https://github.com/pure-admin/vue-pure-admin) 提炼出的架子，更适合实际项目开发，打包后的大小在全局引入 [element-plus](https://element-plus.org) 的情况下仍然低于 `2.3MB`，并且会永久同步完整版的代码。开启 `brotli` 压缩和 `cdn` 替换本地库模式后，打包大小低于 `350kb`

后端是基于flask,采用flask-restful，sqlalchemy，Marshmallow，简单已开发，极易上手，项目开始未进行数据迁移。详见后端配套开发

以实现双token认证，详见auth文件夹


## 前端配套  工作在fronted
### 如果你是前端开发，建议先看vue-pure-admin 官方教程
- [点我查看教程](https://www.bilibili.com/video/BV1kg411v7QT)
- [点我查看 UI 设计](https://www.bilibili.com/video/BV17g411T7rq)

### 配套保姆级文档

- [查看文档](https://yiming_chang.gitee.io/pure-admin-doc)

### 也可以不看 （如果会element-vue3）

比较简单，不赘述，可去官网看目录详情和相关配置

项目开始需构建本地环境
`pnpm install`

运行
`pnpm run dev`
## 后端配套
### 如果你是后端开发，需了解整体框架结构
```- docker-compose.yml  #docker-compose 运行文件
- Dockerfile   
- env_dockerfile  # docker环境文件
- gunicorn.conf   # 项目是由gunicorn启动
- nginx.conf      # 基本nginx
- requirements.txt # python 包文件
- run.py      # 启动入口
- apps
  - __init__.py  # 配置入口
  - auth        # app1
    - models.py # app1 models
    - urls.py  # app1 url
    - __init__.py
    - views  # 视图文件
      - auth.py  # 视图
      - authschema.py  # schema 序列化器
      - __init__.py
  - test # app2
  - utils # 工具文件
    - decorator.py  # 装饰器
    - jwt_util.py  # jwt 认证
    - middlewares.py # 中间件
    - responser.py # 返回格式
    - status.py # 返回状态码
    - __init__.py
- config # 配置文件
  - config.py
  - routes.py  # 所有app 路由出口
- migrations  # 通过flask db init 生成
```
`启动 在backend下执行 python run.py`

## 开发 工作在backend
需构建本地环境，python版本建议3.9以上
`pip install -r requirement.txt` 下载本地环境（记得换源）

本项目是基于flask-restful开发，搭配Marshmallow，需对前端传的数据进行序列化和反序列化，这样做的好处是方便开发，传参，无需从response请求中获取数据。也可对前端传值做校验。

！注意！
在开发一个接口后，须在views同级 url下配置url出口

如

```
auth_api_bp = Blueprint('auth_api', __name__)
auth_api = Api(auth_api_bp)
auth_api.add_resource(AsyncRoute, '/asyncRoutes')
```

还需在config/routes.py 配置总出口

```angular2html
def register_routes(app):
    app.register_blueprint(item_api_bp, url_prefix='/item')
    app.register_blueprint(auth_api_bp, url_prefix='/auth')
新增一行app.register_blueprint 即可
```

！注意！

此版本为做数据迁移
需设置环境变量为`$env:FLASK_APP='run.py'`

做数据迁移初始化`flask db init` 项目周期内只需运行一次

如果新增model 需在apps的配置项中添加，具体见__init__.py 该文件

新增model之后需做 `flask db migrate -m 'create init models'` 做数据迁移

更新使用`flask db upgrade`


## 维护者
Mr.Robot