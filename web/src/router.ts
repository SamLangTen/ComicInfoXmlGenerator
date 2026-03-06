import { createRouter, createWebHistory } from 'vue-router'

// In a simple app, we can just use App.vue to handle routing logic via watch or computed
// But to keep it standard SPA, we'll define routes.
// However, since App.vue currently holds all the state, we'll refactor it slightly 
// to use the URL as the source of truth for activeTab.

const routes = [
  { path: '/', redirect: '/library' },
  { path: '/library', component: { template: '<div></div>' } }, // Handled in App.vue via router view or watch
  { path: '/editor', component: { template: '<div></div>' } },
  { path: '/settings', component: { template: '<div></div>' } },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
