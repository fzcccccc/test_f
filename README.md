# 燕云十六声 - 百业玩法Web系统

这是一个基于Python Flask的Web系统，用于展示燕云十六声游戏中的百业玩法玩家信息。

## 功能特点

- 展示百业玩家列表
- 查看玩家详细信息
- 添加新的百业玩家（包括上传照片）
- 响应式设计，适应不同设备

## 技术栈

- Python 3.7+
- Flask 2.0.1
- Flask-SQLAlchemy 2.5.1
- SQLite数据库

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

然后在浏览器中访问 http://localhost:5000 即可使用系统。

## 项目结构

```
├── app.py                 # 主应用文件
├── requirements.txt       # 项目依赖
├── templates/             # HTML模板
│   ├── base.html          # 基础模板
│   ├── index.html         # 玩家列表页面
│   ├── add_player.html    # 添加玩家页面
│   └── player_detail.html # 玩家详情页面
└── static/                # 静态资源
    ├── placeholder.png    # 默认占位图片
    └── uploads/           # 上传的玩家照片
```

## 说明

- 系统使用SQLite数据库，数据存储在players.db文件中
- 上传的照片保存在static/uploads目录中
- 默认管理员账号：无（本系统无需登录即可使用）