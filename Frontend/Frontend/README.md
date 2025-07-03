# 校园失物招领平台前端

本项目为校园失物招领平台的前端部分，基于 Vue 3 + Vite + Pinia + Vue Router 开发。

## 目录结构

```
src/
├── api/           # API 请求封装
├── assets/        # 静态资源
├── components/    # 公共组件
├── router/        # 路由配置
├── store/         # 状态管理
├── views/         # 页面组件
├── App.vue        # 根组件
└── main.js        # 入口文件
```

## 启动方式

1. 安装依赖

   ```bash
   npm install
   ```

2. 运行开发服务器

   ```bash
   npm run dev
   ```

3. 浏览器访问输出的本地地址（如 http://localhost:5173）

## 技术栈

- [Vue 3](https://vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Pinia](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Axios](https://axios-http.com/)

## 主要功能

- 用户注册、登录、个人中心
- 失物/拾物信息发布、展示、搜索
- 图片上传
- 站内信、智能匹配（预留）

## 目录说明

- `src/api/`：API 请求封装（如 `auth.js`, `items.js`）
- `src/components/`：可复用组件（如 `Navbar.vue`, `ItemCard.vue`）
- `src/views/`：页面级组件（如 `Home.vue`, `Login.vue`）
- `src/router/`：路由配置
- `src/store/`：状态管理
- `src/assets/`：静态资源

## 贡献说明

如需协作开发，请遵循分支管理和代码规范。

---

如有问题请联系项目负责人。
