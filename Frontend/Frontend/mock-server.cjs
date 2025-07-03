const express = require('express')
const cors = require('cors')
const jwt = require('jsonwebtoken')

const app = express()
const PORT = 3001

// 中间件
app.use(cors())
app.use(express.json())

// JWT密钥
const JWT_SECRET = 'your-secret-key'

// 测试用户数据
const testUsers = [
  {
    id: 1,
    username: 'testuser1',
    password: '123456',
    name: '张三',
    studentId: '2021001001',
    phone: '13800138001',
    wechat: 'zhangsan123',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    email: 'zhangsan@example.com'
  },
  {
    id: 2,
    username: 'testuser2',
    password: '123456',
    name: '李四',
    studentId: '2021001002',
    phone: '13800138002',
    wechat: 'lisi456',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    email: 'lisi@example.com'
  },
  {
    id: 3,
    username: 'admin',
    password: 'admin123',
    name: '管理员',
    studentId: '2021001000',
    phone: '13800138000',
    wechat: 'admin001',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    email: 'admin@example.com'
  }
]

// 验证JWT token的中间件
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization']
  const token = authHeader && authHeader.split(' ')[1]

  if (!token) {
    return res.status(401).json({ message: '未提供认证令牌' })
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ message: '令牌无效' })
    }
    req.user = user
    next()
  })
}

// 注册接口
app.post('/api/auth/register', (req, res) => {
  const { username, password, name, studentId, phone, wechat } = req.body

  // 检查用户名是否已存在
  const existingUser = testUsers.find(user => user.username === username)
  if (existingUser) {
    return res.status(400).json({ message: '用户名已存在' })
  }

  // 检查学号是否已存在
  const existingStudentId = testUsers.find(user => user.studentId === studentId)
  if (existingStudentId) {
    return res.status(400).json({ message: '学号已被注册' })
  }

  // 创建新用户
  const newUser = {
    id: testUsers.length + 1,
    username,
    password,
    name,
    studentId,
    phone,
    wechat,
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    email: `${username}@example.com`
  }

  testUsers.push(newUser)

  // 生成JWT token
  const token = jwt.sign(
    { id: newUser.id, username: newUser.username },
    JWT_SECRET,
    { expiresIn: '24h' }
  )

  // 返回用户信息（不包含密码）
  const { password: _, ...userInfo } = newUser

  res.json({
    message: '注册成功',
    token,
    user: userInfo
  })
})

// 登录接口
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body

  // 查找用户
  const user = testUsers.find(u => u.username === username && u.password === password)

  if (!user) {
    return res.status(401).json({ message: '用户名或密码错误' })
  }

  // 生成JWT token
  const token = jwt.sign(
    { id: user.id, username: user.username },
    JWT_SECRET,
    { expiresIn: '24h' }
  )

  // 返回用户信息（不包含密码）
  const { password: _, ...userInfo } = user

  res.json({
    message: '登录成功',
    token,
    user: userInfo
  })
})

// 获取用户信息接口
app.get('/api/auth/me', authenticateToken, (req, res) => {
  const user = testUsers.find(u => u.id === req.user.id)
  
  if (!user) {
    return res.status(404).json({ message: '用户不存在' })
  }

  // 返回用户信息（不包含密码）
  const { password: _, ...userInfo } = user

  res.json({
    user: userInfo
  })
})

// 获取所有用户接口（用于测试）
app.get('/api/users', (req, res) => {
  const usersWithoutPassword = testUsers.map(user => {
    const { password, ...userInfo } = user
    return userInfo
  })
  res.json(usersWithoutPassword)
})

// 测试接口
app.get('/api/test', (req, res) => {
  res.json({ message: 'Mock服务器运行正常' })
})

app.listen(PORT, () => {
  console.log(`Mock服务器运行在 http://localhost:${PORT}`)
  console.log('测试账号信息：')
  testUsers.forEach(user => {
    console.log(`用户名: ${user.username}, 密码: ${user.password}, 姓名: ${user.name}`)
  })
}) 