# 🔧 环境配置指南

在运行项目之前，你需要完成以下配置步骤：

## 📋 必要配置

### 1. 创建 MongoDB Atlas 数据库

#### 步骤1：注册 MongoDB Atlas 账户
1. 访问 [MongoDB Atlas](https://cloud.mongodb.com)
2. 注册免费账户
3. 创建新的项目

#### 步骤2：创建数据库集群
1. 点击 "Build a Database"
2. 选择 **FREE** 共享集群
3. 选择云服务商和区域（推荐选择离你最近的）
4. 集群名称可以保持默认

#### 步骤3：配置数据库访问
1. **创建数据库用户**：
   - 用户名：`your_username`
   - 密码：`your_password` (记住这个密码)
   
2. **配置网络访问**：
   - 点击 "Network Access"
   - 选择 "Add IP Address"
   - 选择 "Allow access from anywhere" (0.0.0.0/0)

#### 步骤4：获取连接字符串
1. 点击 "Database" -> "Connect"
2. 选择 "Connect your application"
3. 选择 Python 3.6+ 版本
4. 复制连接字符串，格式类似：
   ```
   mongodb+srv://your_username:your_password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### 2. 配置环境变量

#### 步骤1：创建 .env 文件
在 `backend/` 目录下创建 `.env` 文件：

```bash
cd backend
# Windows 用户
type nul > .env

# macOS/Linux 用户
touch .env
```

#### 步骤2：填写环境变量
在 `backend/.env` 文件中添加以下内容：

```env
# === 核心配置（必填） ===
MONGO_URI="mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority&appName=Campus-Lost-and-Found-Platform-pro"
JWT_SECRET="your_super_secret_jwt_key_here"

# === 开发配置 ===
FLASK_ENV=development
FLASK_APP=app.py
PORT=5000

# === 邮件配置（可选） ===
MAIL_SERVER=smtp.qq.com
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
MAIL_USERNAME=your_email@qq.com
MAIL_PASSWORD=your_email_app_password
```

#### 步骤3：配置说明

**MONGO_URI（必填）**：
- 将上面获取的 MongoDB 连接字符串填入
- 确保用户名和密码正确

**JWT_SECRET（必填）**：
- 随机生成一个复杂字符串，用于用户认证加密
- 建议长度 > 32 字符，包含字母、数字、符号

**邮件配置（可选）**：
- 如果需要邮件通知功能，需要配置
- QQ邮箱需要使用应用专用密码，不是QQ密码

## 🚀 快速启动

配置完成后：

```bash
# 1. 安装依赖
npm run setup

# 2. 启动项目
npm start
```

## 🔍 故障排除

### 数据库连接失败
1. **检查 MONGO_URI 格式**：确保用户名、密码、集群名称正确
2. **检查网络访问**：确保 IP 地址被允许访问
3. **检查用户权限**：确保数据库用户有读写权限

### 前端无法访问后端
1. **检查端口**：确保后端运行在 5000 端口
2. **检查 CORS 配置**：确保前端域名被允许

### 邮件发送失败
1. **检查邮箱设置**：确保开启了SMTP服务
2. **检查应用密码**：QQ邮箱需要使用应用专用密码

## 📧 获取邮箱应用密码（可选）

### QQ邮箱配置
1. 登录 QQ 邮箱 -> 设置 -> 账户
2. 开启 POP3/SMTP 服务
3. 生成授权码（这就是 MAIL_PASSWORD）

### 163邮箱配置
```env
MAIL_SERVER=smtp.163.com
MAIL_PORT=465
MAIL_USERNAME=your_email@163.com
MAIL_PASSWORD=your_authorization_code
```

## ⚠️ 安全提醒

1. **永远不要**将 `.env` 文件提交到 Git
2. **定期更换** JWT_SECRET 和数据库密码
3. **限制数据库访问**：生产环境中不要使用 0.0.0.0/0
4. **使用强密码**：确保所有密码都足够复杂 
