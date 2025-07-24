<template>
  <div class="p-6 max-w-3xl mx-auto">
    <!-- Header profil -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="flex items-center space-x-4">
        <!-- Avatar -->
        <img :src="avatarUrl" alt="Avatar" class="w-24 h-24 rounded-full border-2 border-blue-500" />

        <!-- Informations principales -->
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ login }}</h1>
          <p class="text-gray-600 dark:text-gray-300">{{ bio }}</p>
          <button @click="toggleTheme"
            class="mt-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
            Passer en {{ isDark ? 'mode clair' : 'mode sombre' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Statistiques fictives -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
      <div class="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg text-center shadow">
        <p class="text-lg font-bold">{{ stats.commandes }}</p>
        <p class="text-gray-700 dark:text-gray-300">Commandes</p>
      </div>
      <div class="bg-green-50 dark:bg-green-900 p-4 rounded-lg text-center shadow">
        <p class="text-lg font-bold">{{ stats.alertes }}</p>
        <p class="text-gray-700 dark:text-gray-300">Alertes</p>
      </div>
      <div class="bg-yellow-50 dark:bg-yellow-900 p-4 rounded-lg text-center shadow">
        <p class="text-lg font-bold">{{ stats.notifications }}</p>
        <p class="text-gray-700 dark:text-gray-300">Notifications</p>
      </div>
    </div>

    <!-- Section préférences (non persistées) -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mt-6">
      <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Préférences locales</h2>
      <div class="mb-4">
        <label class="block mb-1 text-gray-700 dark:text-gray-300">Surnom</label>
        <input v-model="preferences.surnom" type="text" placeholder="Ex: Super Admin"
          class="w-full border border-gray-300 dark:border-gray-700 rounded px-3 py-2 bg-gray-50 dark:bg-gray-700 dark:text-white" />
      </div>
      <div class="mb-4">
        <label class="block mb-1 text-gray-700 dark:text-gray-300">Couleur préférée</label>
        <input v-model="preferences.couleur" type="color"
          class="w-16 h-8 rounded border border-gray-300 dark:border-gray-700 cursor-pointer" />
      </div>
      <button @click="resetPreferences" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
        Réinitialiser
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfilPage',
  data() {
    return {
      login: 'Admin', // login récupéré après connexion
      avatarUrl: 'https://i.pravatar.cc/150?img=12', // avatar fictif
      bio: 'Utilisateur connecté à l’application de gestion.',
      stats: {
        commandes: 12,
        alertes: 3,
        notifications: 5
      },
      preferences: {
        surnom: '',
        couleur: '#1D4ED8'
      },
      isDark: false
    }
  },
  methods: {
    toggleTheme() {
      this.isDark = !this.isDark
      document.documentElement.classList.toggle('dark', this.isDark)
    },
    resetPreferences() {
      this.preferences = {
        surnom: '',
        couleur: '#1D4ED8'
      }
    }
  }
}
</script>

<style scoped>
/* Mode sombre par défaut désactivé */
:root {
  color-scheme: light dark;
}
</style>
