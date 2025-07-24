import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'
import { useMainStore } from '@/stores/main.js'

import './css/main.css'

// Messages de traduction
const messages = {
  en: {
    message: {
      hello: 'hello world',
      gestionProduits: 'Product Management',
      ajouterProduit: 'Add Product',
      exporterCSV: 'Export CSV',
      telechargerPDF: 'Download PDF',
      modifier: 'Edit',
      supprimer: 'Delete',
      gestionVentes: 'Sales Management',
      enregistrerVente: 'Record Sale',
      historiqueVentes: 'Sales History',
      produit: 'Product',
      quantite: 'Quantity',
      dateVente: 'Sale Date',
      parametres: 'Settings',
      langue: 'Language',
      francais: 'French',
      anglais: 'English',
      enregistrer: 'Save',
      annuler: 'Cancel',
    },
  },
  fr: {
    message: {
      hello: 'bonjour le monde',
      gestionProduits: 'Gestion Produits',
      ajouterProduit: 'Ajouter Produit',
      exporterCSV: 'Exporter CSV',
      telechargerPDF: 'Télécharger PDF',
      modifier: 'Modifier',
      supprimer: 'Supprimer',
      gestionVentes: 'Gestion des Ventes',
      enregistrerVente: 'Enregistrer la vente',
      historiqueVentes: 'Historique des Ventes',
      produit: 'Produit',
      quantite: 'Quantité',
      dateVente: 'Date de vente',
      parametres: 'Paramètres',
      langue: 'Langue',
      francais: 'Français',
      anglais: 'Anglais',
      enregistrer: 'Enregistrer',
      annuler: 'Annuler',
    },
  },
}

// Init Pinia
const pinia = createPinia()

// Init i18n
const i18n = createI18n({
  locale: 'fr',
  fallbackLocale: 'fr',
  messages,
})

// Create Vue app
const app = createApp(App)
app.use(router)
app.use(pinia)
app.use(i18n)
app.mount('#app')

// Init main store
const mainStore = useMainStore(pinia)

// Fetch sample data
mainStore.fetchSampleClients()
mainStore.fetchSampleHistory()

// Dark mode
// Uncomment, if you'd like to restore persisted darkMode setting, or use `prefers-color-scheme: dark`. Make sure to uncomment localStorage block in src/stores/darkMode.js
// import { useDarkModeStore } from './stores/darkMode'

// const darkModeStore = useDarkModeStore(pinia)

// if (
//   (!localStorage['darkMode'] && window.matchMedia('(prefers-color-scheme: dark)').matches) ||
//   localStorage['darkMode'] === '1'
// ) {
//   darkModeStore.set(true)
// }

// Default title tag
const defaultDocumentTitle = 'Admin One Vue 3 Tailwind'

// Set document title from route meta
router.afterEach((to) => {
  document.title = to.meta?.title
    ? `${to.meta.title} — ${defaultDocumentTitle}`
    : defaultDocumentTitle
})
