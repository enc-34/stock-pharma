<template>
  <div class="rounded-lg p-6">
    <div class="flex flex-wrap justify-between items-center mb-4 space-y-2 md:space-y-0">
      <h1 class="text-2xl font-bold">Historique des Mouvements</h1>
      <div class="flex flex-wrap gap-2 items-center">
        <input v-model="searchQuery" type="text" placeholder="Rechercher (produit/type)..."
          class="border border-gray-300 rounded px-3 py-2 w-64" />
        <input v-model="startDate" type="date" class="border border-gray-300 rounded px-3 py-2" />
        <input v-model="endDate" type="date" class="border border-gray-300 rounded px-3 py-2" />
        <button @click="resetFilters"
          class="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300 transition">Réinitialiser</button>
      </div>
    </div>

    <table class="w-full border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Produit</th>
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Type</th>
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Quantité</th>
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Date</th>
          <!-- <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Utilisateur</th> -->
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Remarque</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mouvement in paginatedMouvements" :key="mouvement.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ mouvement.produit_nom }}</td>
          <td class="py-2 px-4 border-b">
            <span :class="typeBadgeClass(mouvement.type_mouvement)">
              {{ mouvement.type_mouvement }}
            </span>
          </td>
          <td class="py-2 px-4 border-b">{{ mouvement.quantite }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(mouvement.date) }}</td>
          <!-- <td class="py-2 px-4 border-b">{{ mouvement.utilisateur || 'N/A' }}</td> -->
          <td class="py-2 px-4 border-b">
            <input type="text" v-model="mouvement.remarque" @blur="updateRemarque(mouvement)"
              class="w-full border border-gray-300 rounded px-2 py-1 text-sm" placeholder="Ajouter une remarque" />
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="flex justify-center space-x-2 mt-4">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1"
        class="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100 disabled:opacity-50">
        Précédent
      </button>
      <button v-for="page in totalPages" :key="page" @click="changePage(page)"
        :class="['px-3 py-1 rounded border border-gray-300 hover:bg-gray-100', { 'bg-gray-300': currentPage === page }]">
        {{ page }}
      </button>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages"
        class="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100 disabled:opacity-50">
        Suivant
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HistoriqueMouvementsPage',
  data() {
    return {
      mouvements: [],
      searchQuery: '',
      startDate: '',
      endDate: '',
      currentPage: 1,
      pageSize: 8,
      isSaving: false,
    }
  },
  computed: {
    filteredMouvements() {
      return this.mouvements.filter(m => {
        const query = this.searchQuery.toLowerCase()
        const dateM = new Date(m.date_mouvement)

        const matchQuery =
          !this.searchQuery ||
          m.produit.nom.toLowerCase().includes(query) ||
          m.type.toLowerCase().includes(query)

        const matchDate =
          (!this.startDate || dateM >= new Date(this.startDate)) &&
          (!this.endDate || dateM <= new Date(this.endDate + 'T23:59:59'))

        return matchQuery && matchDate
      })
    },
    totalPages() {
      return Math.ceil(this.filteredMouvements.length / this.pageSize)
    },
    paginatedMouvements() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredMouvements.slice(start, start + this.pageSize)
    }
  },
  methods: {
    async fetchMouvements() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/mouvements/')
        this.mouvements = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des mouvements:', error)
      }
    },
    async updateRemarque(mouvement) {
      if (this.isSaving) return
      this.isSaving = true
      try {
        await axios.patch(`http://127.0.0.1:8000/api/mouvements/${mouvement.id}/`, {
          remarque: mouvement.remarque,
        })
      } catch (error) {
        console.error('Erreur lors de la mise à jour de la remarque:', error)
        alert('Erreur lors de la mise à jour de la remarque')
      } finally {
        this.isSaving = false
      }
    },
    resetFilters() {
      this.searchQuery = ''
      this.startDate = ''
      this.endDate = ''
      this.currentPage = 1
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },
    typeBadgeClass(type) {
      return type === 'ENTREE'
        ? 'text-green-700 bg-green-100 px-2 py-1 rounded'
        : 'text-red-700 bg-red-100 px-2 py-1 rounded'
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  },
  mounted() {
    this.fetchMouvements()
  }
}
</script>
