# Campus-Lost-and-Found-Platform-pro
# 🎓 校园失物招领平台

一个专为高校师生设计的失物招领平台，帮助大家快速找回丢失物品，建设温暖的校园互助社区。

![项目状态](https://img.shields.io/badge/状态-开发中-green)
![前端](https://img.shields.io/badge/前端-Vue.js%203-4FC08D)
![后端](https://img.shields.io/badge/后端-Flask-000000)
![数据库](https://img.shields.io/badge/数据库-SQLite-003B57)

## 📸 项目预览

*（这里可以添加项目截图）*

## ✨ 功能特性

### 🔐 用户系统
- **用户注册/登录** - 支持学号验证的安全认证
- **个人中心** - 头像上传、个人信息管理
- **权限管理** - 基于JWT的身份验证

### 📝 物品管理
- **发布失物/拾物** - 详细的物品信息录入
- **智能分类** - 多种物品类型分类管理
- **图片上传** - 支持多图片展示
- **状态跟踪** - 丢失/拾取/已认领状态管理

### 💬 互动功能
- **站内消息** - 安全的用户间沟通
- **联系方式** - 多种联系方式（微信、电话）
- **评论系统** - 帖子评论互动

### 🗺️ 地图定位
- **位置标记** - 物品丢失/拾取地点标记
- **地图展示** - 直观的地理位置信息

### 🔍 搜索功能
- **关键词搜索** - 快速定位相关物品
- **分类筛选** - 按类型、状态等条件筛选
- **智能匹配** - 失物与拾物智能配对（开发中）

## 🛠️ 技术栈

### 前端技术
- **框架**: Vue.js 3 + Composition API
- **构建工具**: Vite 7.0
- **UI组件**: Element Plus 2.10
- **状态管理**: Pinia 3.0
- **路由**: Vue Router 4.5
- **HTTP客户端**: Axios 1.10
- **样式**: CSS3 + 响应式设计

### 后端技术
- **框架**: Flask (Python)
- **数据库**: SQLite
- **认证**: JWT (JSON Web Token)
- **文件上传**: Flask 内置文件处理
- **跨域**: Flask-CORS
- **邮件服务**: Flask-Mail

### 开发工具
- **并发运行**: Concurrently
- **包管理**: npm + pip
- **版本控制**: Git
- **代码编辑**: VS Code (推荐)

## 📦 快速开始

### 环境要求
- **Node.js**: >= 16.0.0
- **Python**: >= 3.8
- **npm**: >= 8.0.0
- **Git**: 最新版本

### 一键安装与启动

```bash
# 1. 克隆项目
git clone https://github.com/SunXiangyuNico/Campus-Lost-and-Found-Platform-pro.git
cd Campus-Lost-and-Found-Platform-pro

# 2. 安装所有依赖
npm run setup

# 3. 启动整个项目（前端 + 后端）
npm start
```

### 分步安装

```bash
# 安装根目录依赖（项目管理工具）
npm install

# 安装前端依赖
npm run install:frontend

# 安装后端依赖
npm run install:backend
```

### 分别启动服务

```bash
# 启动前端开发服务器 (http://localhost:5173)
npm run dev:frontend

# 启动后端服务器 (http://localhost:5000)
npm run dev:backend

# 启动Mock测试服务器 (http://localhost:3001)
npm run dev:mock
```

## 🧪 测试账号

| 角色 | 用户名 | 密码 | 姓名 | 学号 |
|------|--------|------|------|------|
| 普通用户 | testuser1 | 123456 | 张三 | 2021001001 |
| 普通用户 | testuser2 | 123456 | 李四 | 2021001002 |
| 管理员 | admin | admin123 | 管理员 | 2021001000 |

## 📁 项目结构

```
Campus-Lost-and-Found-Platform/
├── 📄 README.md                  # 项目说明文档
├── 📄 package.json               # 根目录项目配置
├── 📄 package-lock.json          # 依赖版本锁定
├── 📄 .gitignore                 # Git忽略配置
│
├── 📁 Frontend/Frontend/          # 前端项目
│   ├── 📄 package.json           # 前端依赖配置
│   ├── 📄 vite.config.js         # Vite构建配置
│   ├── 📄 index.html             # HTML入口文件
│   ├── 📁 src/                   # 前端源码
│   │   ├── 📄 main.js            # 前端入口
│   │   ├── 📄 App.vue            # 根组件
│   │   ├── 📁 components/        # 可复用组件
│   │   ├── 📁 views/             # 页面组件
│   │   ├── 📁 router/            # 路由配置
│   │   ├── 📁 store/             # 状态管理
│   │   ├── 📁 api/               # API封装
│   │   └── 📁 utils/             # 工具函数
│   ├── 📁 public/                # 静态资源
│   └── 📄 mock-server.cjs        # Mock测试服务器
│
└── 📁 backend/                   # 后端项目
    ├── 📄 app.py                 # Flask应用入口
    ├── 📄 requirements.txt       # Python依赖
    ├── 📁 config/                # 配置文件
    ├── 📁 models/                # 数据模型
    ├── 📁 routes/                # 路由定义
    ├── 📁 controllers/           # 控制器
    ├── 📁 middleware/            # 中间件
    ├── 📁 services/              # 业务服务
    └── 📁 static/                # 静态文件存储
        ├── 📁 uploads/           # 用户上传文件
        └── 📁 avatars/           # 用户头像
```

## 🚀 部署指南

### 开发环境
```bash
npm start  # 启动完整开发环境
```

### 生产环境
```bash
# 构建前端
npm run build:frontend

# 启动后端生产服务器
cd backend
python app.py
```

## 📖 API文档

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 物品接口
- `GET /api/items` - 获取物品列表
- `POST /api/items` - 发布新物品
- `PUT /api/items/:id` - 更新物品信息
- `DELETE /api/items/:id` - 删除物品

### 消息接口
- `GET /api/messages` - 获取消息列表
- `POST /api/messages` - 发送消息

*更多API详情请参考各模块文档*

## 🧭 开发指南

### 前端开发
```bash
cd Frontend/Frontend
npm run dev  # 启动开发服务器
```

### 后端开发
```bash
cd backend
python app.py  # 启动Flask应用
```

### 代码规范
- 前端：遵循Vue.js官方风格指南
- 后端：遵循PEP 8 Python编码规范
- 提交：使用语义化提交信息

### 调试技巧
1. **前端调试**: 使用浏览器DevTools + Vue DevTools
2. **后端调试**: Flask内置调试模式
3. **网络调试**: 检查浏览器Network面板
4. **状态调试**: 使用Pinia DevTools

## 🧪 测试

### Mock服务器测试
```bash
npm run dev:mock  # 启动Mock服务器进行前端测试
```

### 功能测试清单
- [ ] 用户注册/登录
- [ ] 物品发布/编辑/删除
- [ ] 消息收发
- [ ] 图片上传
- [ ] 地图定位
- [ ] 搜索筛选

## 🤝 贡献指南

### 提交代码
1. Fork 本仓库
2. 创建特性分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送到分支: `git push origin feature/AmazingFeature`
5. 创建Pull Request

### 报告问题
请通过[Issues](https://github.com/your-username/Campus-Lost-and-Found-Platform/issues)报告bug或提出建议。

## 📞 联系我们

- **项目维护者**: [Your Name]
- **邮箱**: your.email@example.com
- **项目地址**: [GitHub仓库链接]

## 📜 开源协议

本项目基于 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和测试用户！

---

⭐ 如果这个项目对你有帮助，请给我们一个Star！

🔗 **相关链接**
- [Vue.js 官方文档](https://vuejs.org/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Element Plus 组件库](https://element-plus.org/)
- [Pinia 状态管理](https://pinia.vuejs.org/) 
