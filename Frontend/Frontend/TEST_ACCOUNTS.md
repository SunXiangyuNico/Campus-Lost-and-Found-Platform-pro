# 测试账号数据

## 启动Mock服务器

1. 安装依赖：
```bash
npm install express cors jsonwebtoken
```

2. 启动服务器：
```bash
node mock-server.js
```

服务器将在 http://localhost:3001 运行

## 测试账号信息

### 账号1
- **用户名**: testuser1
- **密码**: 123456
- **姓名**: 张三
- **学号**: 2021001001
- **电话**: 13800138001
- **微信号**: zhangsan123

### 账号2
- **用户名**: testuser2
- **密码**: 123456
- **姓名**: 李四
- **学号**: 2021001002
- **电话**: 13800138002
- **微信号**: lisi456

### 管理员账号
- **用户名**: admin
- **密码**: admin123
- **姓名**: 管理员
- **学号**: 2021001000
- **电话**: 13800138000
- **微信号**: admin001

## API接口

### 登录
- **URL**: POST /api/auth/login
- **参数**: { username, password }

### 注册
- **URL**: POST /api/auth/register
- **参数**: { username, password, name, studentId, phone, wechat }

### 获取用户信息
- **URL**: GET /api/auth/me
- **需要**: Authorization: Bearer {token}

### 获取所有用户（测试用）
- **URL**: GET /api/users

## 使用说明

1. 确保mock服务器正在运行
2. 在前端应用中使用上述测试账号进行登录
3. 登录成功后可以测试各种功能，包括：
   - 查看帖子详情
   - 点击"联系拾主"按钮（需要登录）
   - 发表评论（需要登录）
   - 发布新帖子

## 注意事项

- 所有测试数据都存储在内存中，重启服务器后数据会重置
- JWT token有效期为24小时
- 密码是明文存储的，仅用于测试目的 