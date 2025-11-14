import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/workflow/:id?',
    name: 'WorkflowEditor',
    component: () => import('../views/WorkflowEditor.vue')
  },
  {
    path: '/tools',
    name: 'ToolManagement',
    component: () => import('../views/ToolManagement.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
