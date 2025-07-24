import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/api/auth.js'
import Login from '@/pages/Login.vue'
import Dashboard from '@/pages/Dashboard.vue'
import Produits from '@/pages/Produits.vue'
import Categories from '@/pages/Categories.vue'
import Fournisseurs from '@/pages/Fournisseurs.vue'
import Mouvements from '@/pages/Mouvements.vue'
import Parametre from '@/pages/Parametre.vue'
import HistoriquesMouvements from '@/pages/HistoriquesMouvements.vue'
import BarcodeScanner from '@/pages/BarcodeScanner.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/produits', name: 'Produits', component: Produits },
  { path: '/categories', name: 'Categories', component: Categories },
  { path: '/fournisseurs', name: 'Fournisseurs', component: Fournisseurs },
  { path: '/mouvements', name: 'Mouvements', component: Mouvements },
  { path: '/parametre', name: 'Parametre', component: Parametre },
  {
    path: '/historiques-mouvements',
    name: 'HistoriquesMouvements',
    component: HistoriquesMouvements,
  },
  {
    path: '/barcode-scanner',
    name: 'BarcodeScanner',
    component: BarcodeScanner,
  },
  {
    path: '/historique-ventes',
    name: 'HistoriqueVentes',
    component: () => import('@/pages/HistoriqueVentes.vue'),
  },
  {
    path: '/ventes',
    name: 'Ventes',
    component: () => import('@/pages/Ventes.vue'),
  },
  {
    path: '/approvisionnements-auto',
    name: 'ApprovisionnementsAuto',
    component: () => import('@/pages/ApprovisionnementsAuto.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/pages/Profile.vue'),
  },
  {
    path: '/commandes-fournisseurs',
    name: 'CommandesFournisseurs',
    component: () => import('@/pages/CommandesFournisseurs.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

// Guard : redirection si pas connecté
router.beforeEach((to, from, next) => {
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const token = getToken()

  if (authRequired && !token) {
    return next('/login')
  }
  next()
})

export default router
