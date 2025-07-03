# 登录检查功能实现

## 功能描述
在用户未登录状态下点击导航栏的"发布"按钮时，系统会显示提示信息"请先登录后再发布信息"，而不是直接打开发布对话框。

## 实现位置
- 文件：`src/components/Navbar.vue`
- 函数：`goPublish()`

## 实现逻辑
1. 在 `goPublish()` 函数中添加登录状态检查
2. 使用 `isLogin` 计算属性判断用户是否已登录
3. 如果未登录，显示 Element Plus 的警告消息
4. 如果已登录，正常触发发布事件

## 代码修改
```javascript
function goPublish() {
  if (!isLogin.value) {
    ElMessage.warning('请先登录后再发布信息')
    return
  }
  emit('publish')
}
```

## 依赖
- Element Plus 的 `ElMessage` 组件用于显示提示信息
- 用户状态管理 store (`useUserStore`) 用于获取登录状态

## 用户体验
- 未登录用户点击发布按钮时会看到友好的提示信息
- 提示信息使用警告样式，符合用户预期
- 不会打断用户的其他操作流程 