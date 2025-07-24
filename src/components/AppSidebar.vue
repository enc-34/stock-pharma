<template>
  <div class="flex">
    <!-- SIDEBAR -->
    <aside
      :class="['fixed top-0 left-0 h-screen bg-gray-400 text-white z-50 transition-all duration-300', collapsed ? 'w-20' : 'w-64']">
      <!-- Logo et bouton de collapse -->
      <div class="flex items-center justify-between p-4 border-b border-gray-700">
        <h1 class="text-xl font-bold tracking-wide" v-if="!collapsed">STOCKAPP</h1>
        <button @click="toggleSidebar" class="p-1 rounded hover:bg-gray-700">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Liens -->
      <nav class="mt-4">
        <ul>
          <li v-for="link in links" :key="link.name" class="mb-1">
            <router-link :to="link.to"
              class="flex items-center gap-3 px-4 py-3 hover:bg-gray-700 rounded transition-colors">
              <span v-html="link.icon"></span>
              <span v-if="!collapsed">{{ link.name }}</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- CONTENU -->
    <div :class="['transition-all duration-300 flex-1', collapsed ? 'ml-20' : 'ml-64']">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppSidebar',
  data() {
    return {
      collapsed: false,
      links: [
        {
          name: 'Dashboard',
          to: '/dashboard',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M13 5v6h6" />
                 </svg>`
        },
        {
          name: 'Produits',
          to: '/produits',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V7a2 2 0 00-2-2H6a2 2 0 00-2 2v6" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 17H8a2 2 0 01-2-2v-1h12v1a2 2 0 01-2 2z" />
                 </svg>`
        },
        {
          name: 'Fournisseurs',
          to: '/fournisseurs',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-3-3.87" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 20H4v-2a4 4 0 013-3.87" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 12a4 4 0 100-8 4 4 0 000 8z" />
                 </svg>`
        },
        {
          name: 'Commandes Fournisseurs',
          to: '/commandes-fournisseurs',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 17l-3-3m0 0l3-3m-3 3h12" />
                 </svg>`
        },
        {
          name: 'Catégories',
          to: '/categories',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                 </svg>`
        },
        {
          name: 'Mouvements',
          to: '/mouvements',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 6h18M3 14h18M3 18h18" />
                 </svg>`
        },

        {
          name: 'Approvisionnements Auto',
          to: '/approvisionnements-auto',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v16h16" />
                 </svg>`
        },
        {
          name: 'Paramètres',
          to: '/parametre',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v1m6.364 1.636l-.707.707M20 12h-1M17.657 17.657l-.707-.707M12 19v1M6.343 17.657l.707-.707M4 12H3m3.636-4.364l.707.707M12 7a5 5 0 100 10 5 5 0 000-10z" />
                 </svg>`
        },
        {
          name: 'Code Barre',
          to: '/barcode-scanner',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 4h1v16H3zM6 4h2v16H6zM10 4h1v16h-1zM13 4h2v16h-2zM17 4h1v16h-1zM20 4h1v16h-1z" />
                 </svg>`
        },
        {
          name: 'Ventes',
          to: '/ventes',
          icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 6h18M3 14h18M3 18h18" />
                 </svg>`
        }

      ],

      methods: {
        toggleSidebar() {
          this.collapsed = !this.collapsed
        }
      }
    };
  },
  computed: {
    sidebarWidth() {
      return this.collapsed ? 'w-20' : 'w-64';
    },
  }
}
</script>

<style scoped>
/* Transition du contenu quand la sidebar est réduite */
</style>
