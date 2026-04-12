import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MainView from '../views/MainView.vue'
import AdminView from '../views/AdminView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/main',
      name: 'main',
      component: MainView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    }
  ]
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const isLoggedIn = !!user

  // 需要登录的页面
  const authRequired = ['/main', '/history', '/admin']
  // 需要管理员权限的页面
  const adminRequired = ['/admin']

  if (authRequired.includes(to.path) && !isLoggedIn) {
    // 未登录 → 跳回登录页
    return next('/')
  }

  if (adminRequired.includes(to.path) && (!user || !user.is_admin)) {
    // 非管理员访问 /admin → 跳回主页
    return next('/main')
  }

  if (to.path === '/' && isLoggedIn) {
    // 已登录用户访问登录页 → 直接去主页
    return next('/main')
  }

  next()
})

export default router
