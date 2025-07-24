<script setup>
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import menu from '@/menuNavBarMinimal.js'
import { logout } from '@/api/auth.js'

const router = useRouter()

const menuClick = (event, item) => {
  if (item.isLogout) {
    logout()
    router.push('/login')
  }
}
</script>

<template>
  <header
    class="header-component flex justify-between items-center px-6 py-3 bg-white dark:bg-slate-800 shadow-md"
  >
    <!-- LOGO + TITRE -->
    <div class="flex items-center space-x-3">

      <h1 class="text-xl font-bold text-gray-800 dark:text-gray-100">
        Tableau de Bord
      </h1>
    </div>

    <!-- MENU NAVIGATION -->
    <NavBar :menu="menu" @menu-click="menuClick" />

    <!-- PROFIL UTILISATEUR -->
    <div class="flex items-center space-x-4">
      <!-- Bouton Thème -->
      <button
        class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 dark:bg-slate-700 dark:hover:bg-slate-600"
        @click="$emit('toggle-theme')"
        title="Changer le thème"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-gray-600 dark:text-gray-300"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 3v1m0 16v1m8.485-8.485h-1M4.515 12.515h-1M16.95 7.05l-.707.707M7.757 16.243l-.707.707M16.95 16.95l-.707-.707M7.757 7.757l-.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z"
          />
        </svg>
      </button>

      <!-- Avatar -->
      <div class="flex items-center space-x-2">
        <img
          src="https://ui-avatars.com/api/?name=Utilisateur&background=random"
          alt="Avatar"
          class="h-8 w-8 rounded-full"
        />
        <div class="text-sm text-gray-700 dark:text-gray-300">
          <p class="font-semibold">Utilisateur</p>
          <p class="text-xs text-gray-500">Admin</p>
        </div>
      </div>

      <!-- Déconnexion -->
      <button
        @click="menuClick($event, { isLogout: true })"
        class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
      >
        Déconnexion
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
}
</script>

<style scoped>
.header-component {
  transition: all 0.3s ease;
}
</style>
