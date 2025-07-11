# 登录注册功能测试说明

## 🎯 功能实现

### 1. 导航栏按钮
- ✅ **登录按钮**: 位于导航栏右侧，未登录时显示
- ✅ **注册按钮**: 位于登录按钮旁边，未登录时显示
- ✅ **发布按钮**: 主要操作按钮，样式更醒目

### 2. 登录功能
- ✅ **登录对话框**: 点击登录按钮弹出
- ✅ **表单验证**: 用户名和密码必填验证
- ✅ **切换注册**: 点击"立即注册"可切换到注册对话框
- ✅ **成功提示**: 登录成功后显示成功消息

### 3. 注册功能
- ✅ **注册对话框**: 点击注册按钮弹出
- ✅ **表单验证**: 
  - 姓名：必填
  - 学号：8-12位数字
  - 密码：至少6位
  - 电话：6-15位数字
  - 微信号：必填
- ✅ **切换登录**: 点击"去登录"可切换到登录对话框
- ✅ **成功提示**: 注册成功后显示成功消息

## 🧪 测试步骤

### 测试登录功能
1. 打开浏览器访问 `http://localhost:5176/`
2. 点击导航栏右侧的"登录"按钮
3. 验证登录对话框是否正常弹出
4. 测试表单验证：
   - 不输入任何内容直接点击登录
   - 只输入用户名不输入密码
   - 只输入密码不输入用户名
5. 点击"立即注册"测试切换功能
6. 输入有效信息后点击登录，查看成功提示

### 测试注册功能
1. 点击导航栏右侧的"注册"按钮
2. 验证注册对话框是否正常弹出
3. 测试表单验证：
   - 测试学号格式（输入非数字、少于8位、超过12位）
   - 测试密码长度（少于6位）
   - 测试电话号码格式
   - 测试必填字段
4. 点击"去登录"测试切换功能
5. 输入有效信息后点击注册，查看成功提示

### 测试按钮状态
1. 验证未登录状态下显示"登录"和"注册"按钮
2. 验证登录状态下隐藏"登录"和"注册"按钮，显示用户信息

## 🎨 界面特点

### 按钮样式
- **登录/注册按钮**: 文本按钮样式，悬停时变蓝色
- **发布按钮**: 主要按钮样式，蓝色背景，带图标
- **响应式设计**: 在小屏幕上按钮会自适应

### 对话框样式
- **现代化设计**: 使用Element Plus的对话框组件
- **表单验证**: 实时验证和错误提示
- **切换功能**: 登录和注册之间可以无缝切换

## 🔧 技术实现

### 组件结构
```
Home.vue
├── Navbar.vue (导航栏)
├── Login.vue (登录对话框)
├── Register.vue (注册对话框)
└── 其他组件...
```

### 事件通信
- 导航栏通过 `emit` 向主页发送事件
- 主页监听事件并控制对话框显示
- 登录和注册对话框之间可以相互切换

### 表单验证
- 使用Element Plus的表单验证规则
- 实时验证和提交时验证
- 友好的错误提示信息

## 🚀 使用说明

1. **登录流程**:
   - 点击"登录"按钮
   - 输入用户名和密码
   - 点击"登录"按钮
   - 查看成功提示

2. **注册流程**:
   - 点击"注册"按钮
   - 填写完整的注册信息
   - 确保所有字段验证通过
   - 点击"注册"按钮
   - 查看成功提示

3. **切换功能**:
   - 在登录对话框中点击"立即注册"
   - 在注册对话框中点击"去登录"
   - 对话框会自动切换

## 📱 响应式支持

- **桌面端**: 完整的按钮和对话框显示
- **平板端**: 按钮和对话框自适应
- **移动端**: 对话框宽度自适应，按钮布局优化

---

*现在你可以测试登录和注册功能了！点击导航栏的"登录"或"注册"按钮即可体验。* 