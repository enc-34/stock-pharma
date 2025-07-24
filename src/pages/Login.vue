<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white p-8 rounded shadow">
      <h2 class="text-2xl font-bold mb-6 text-center flex items-center justify-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24"
          stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 01-8 0 4 4 0 018 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 14v7m0 0H9m3 0h3" />
        </svg>
        <span>Connexion</span>
      </h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="username" class="block text-gray-700">Nom d'utilisateur</label>
          <div class="relative mt-1">
            <input id="username" v-model="username" type="text" required
              class="w-full border border-gray-300 rounded-lg pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <svg xmlns="http://www.w3.org/2000/svg"
              class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none"
              viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M5.121 17.804A13.937 13.937 0 0112 15c2.5 0 4.847.655 6.879 1.804M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-700">Mot de passe</label>
          <div class="relative mt-1">
            <input id="password" v-model="password" type="password" required
              class="w-full border border-gray-300 rounded-lg pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <svg xmlns="http://www.w3.org/2000/svg"
              class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none"
              viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 11c0-1.105-.895-2-2-2s-2 .895-2 2v1h4v-1zM12 11v1a2 2 0 11-4 0v-1a2 2 0 114 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 11v1a2 2 0 104 0v-1a2 2 0 00-4 0z" />
            </svg>
          </div>
        </div>
        <div v-if="error" class="mb-4 text-red-600 text-sm">{{ error }}</div>
        <button type="submit" class="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          :disabled="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { login, saveToken } from '@/api/auth.js'

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false,
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.loading = true
      try {
        const response = await login(this.username, this.password)
        saveToken(response.data.access)
        this.$router.push({ name: 'Dashboard' })
      } catch {
        this.error = 'Nom d\'utilisateur ou mot de passe incorrect.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped></style>
