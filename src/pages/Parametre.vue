<template>
  <section class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
      <!-- Header -->
      <header class="flex items-center justify-between border-b pb-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Paramètres</h1>
          <p class="text-sm text-gray-500">Bienvenue sur la page des paramètres</p>
        </div>
        <button @click="saveSettings"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
          Enregistrer
        </button>
      </header>

      <!-- Tabs -->
      <nav class="flex space-x-6 border-b mb-6 text-gray-500">
        <button v-for="tab in tabs" :key="tab" @click="currentTab = tab" :class="[
          'pb-2 transition',
          currentTab === tab
            ? 'border-b-2 border-indigo-600 text-indigo-600 font-medium'
            : 'hover:text-indigo-600'
        ]">
          {{ tab }}
        </button>
      </nav>

      <!-- Contenu dynamique -->
      <div class="space-y-6">
        <!-- Profil -->
        <div v-if="currentTab === 'Profil'" class="bg-gray-50 p-5 rounded-xl shadow-sm">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Informations du profil</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-600">Nom</label>
              <input v-model="settings.name" type="text" placeholder="John Doe"
                class="mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring focus:border-indigo-300" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-600">Email</label>
              <input v-model="settings.email" type="email" placeholder="john@example.com"
                class="mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring focus:border-indigo-300" />
            </div>
          </div>
        </div>

        <!-- Sécurité -->
        <div v-if="currentTab === 'Sécurité'" class="bg-gray-50 p-5 rounded-xl shadow-sm">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Sécurité</h3>
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Authentification à deux facteurs</span>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.twoFactor" class="sr-only peer">
              <div
                class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-indigo-500 rounded-full peer peer-checked:bg-indigo-600 transition-all">
              </div>
              <div
                class="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-all peer-checked:translate-x-5">
              </div>
            </label>
          </div>
        </div>

        <!-- Notifications -->
        <div v-if="currentTab === 'Notifications'" class="bg-gray-50 p-5 rounded-xl shadow-sm">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Notifications</h3>
          <label class="flex items-center space-x-3">
            <input type="checkbox" v-model="settings.emailUpdates"
              class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500">
            <span class="text-gray-600">Recevoir des emails de mise à jour</span>
          </label>
          <label class="flex items-center space-x-3 mt-2">
            <input type="checkbox" v-model="settings.pushNotifications"
              class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500">
            <span class="text-gray-600">Notifications push</span>
          </label>
        </div>

        <!-- Préférences -->
        <div v-if="currentTab === 'Préférences'" class="bg-gray-50 p-5 rounded-xl shadow-sm">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Préférences</h3>
          <label class="block mb-2 text-sm text-gray-600">Thème</label>
          <select v-model="settings.theme"
            class="p-2 border rounded-lg focus:outline-none focus:ring focus:border-indigo-300">
            <option value="clair">Clair</option>
            <option value="sombre">Sombre</option>
            <option value="auto">Automatique</option>
          </select>

          <!-- Langue -->
          <div class="mt-6">
            <label class="block mb-2 text-sm text-gray-600">Langue</label>
            <select v-model="settings.language" @change="changeLanguage"
              class="p-2 border rounded-lg focus:outline-none focus:ring focus:border-indigo-300">
              <option value="fr">Français</option>
              <option value="en">Anglais</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, watch, onMounted, getCurrentInstance } from 'vue'

defineOptions({
  name: 'PageParametre'
})
// Liste des onglets
const tabs = ['Profil', 'Sécurité', 'Notifications', 'Préférences']

// Onglet actif
const currentTab = ref('Profil')

// État des paramètres
const settings = ref({
  name: 'Manuella DONGMO',
  email: 'manuelladongmo.com',
  twoFactor: false,
  emailUpdates: true,
  pushNotifications: false,
  theme: 'clair',
  language: 'fr'
})

// Fonction pour changer le thème
const applyTheme = () => {
  const html = document.documentElement
  if (settings.value.theme === 'sombre') {
    html.classList.add('dark')
  } else if (settings.value.theme === 'clair') {
    html.classList.remove('dark')
  } else {
    // Mode auto = basé sur les préférences système
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }
}

// Appliquer le thème initialement
onMounted(() => applyTheme())

// Réagir aux changements
watch(() => settings.value.theme, applyTheme)

// Fonction pour changer la langue
const changeLanguage = () => {
  const { proxy } = getCurrentInstance()
  proxy.$i18n.locale = settings.value.language
}

// Fonction pour enregistrer (simulation)
const saveSettings = () => {
  console.log('Paramètres enregistrés :', settings.value)
  alert('Paramètres enregistrés avec succès !')
}
</script>
