# Campus Buzz Mini Project

这是一个基于 Flask 和 Docker Compose 的校园活动提交与处理系统，由三个服务组成：

- `presentation-service`：页面展示服务，提供活动提交表单和结果页面。
- `workflow-service`：流程服务，接收提交内容，写入数据服务，并触发事件处理函数。
- `data-service`：数据服务，负责保存、查询和更新活动记录。

## 项目结构

```text
.
├── data-service/
├── workflow-service/
├── presentation-service/
├── data/
├── docker-compose.yml
└── README.md
```

## 运行方式

确保本机已经安装 Docker Desktop，然后在项目根目录运行：

```powershell
docker compose up --build
```

启动后访问：

```text
http://localhost
```

## 服务端口

- `presentation-service`：宿主机 `80`，容器内 `5000`
- `workflow-service`：`5001`
- `data-service`：`5002`

## 上传说明

上传 GitHub 时只需要提交源码、配置文件和说明文档，不需要提交虚拟环境、IDE 配置、打包后的依赖目录或 zip 文件。
