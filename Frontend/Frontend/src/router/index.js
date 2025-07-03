import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  { path: '/', name: 'Welcome', component: () => import('../views/Welcome.vue') },
  { path: '/home', name: 'Home', component: () => import('../views/Home.vue') },
  // { path: '/login', name: 'Login', component: () => import('../views/Login.vue') }, // 已删除
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  { path: '/profile', name: 'UserProfile', component: () => import('../views/UserProfile.vue') },
  { path: '/messages', name: 'Messages', component: () => import('../views/Messages.vue') },
  { path: '/debug', name: 'Debug', component: () => import('../views/Debug.vue') },
  // { path: '/new', name: 'NewPost', component: () => import('../views/NewPost.vue') }, // 已废弃，已删除
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  console.log(`=== 路由守卫：从 ${from.path} 到 ${to.path} ===`)
  
  const userStore = useUserStore()
  
  // 如果目标是欢迎页面且用户已登录，跳转到主页
  if (to.name === 'Welcome' && userStore.isLogin) {
    console.log('用户已登录，从欢迎页面跳转到主页')
    next('/home')
    return
  }
  
  // 需要登录才能访问的页面
  const requireAuthPages = ['UserProfile', 'Messages']
  
  // 如果访问需要登录的页面但未登录，跳转到欢迎页面
  if (requireAuthPages.includes(to.name) && !userStore.isLogin) {
    console.log('需要登录，跳转到欢迎页面')
    next('/')
    return
  }
  
  // 其他情况直接通过
  console.log('路由守卫通过')
  next()
})

export default router 