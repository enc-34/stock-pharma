<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Historique des Ventes</h1>
      <input v-model="searchQuery" type="text" placeholder="Rechercher un produit..."
        class="border border-gray-300 rounded px-3 py-2 mr-4" />
      <button @click="openModal()"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Vente</span>
      </button>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Produit</th>
          <th class="border border-gray-300 dark:border-gray-600">Quantité</th>
          <th class="border border-gray-300 dark:border-gray-600">Date de Vente</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="vente in paginatedVentes" :key="vente.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ vente.produit_nom }}</td>
          <td class="py-2 px-4 border-b">{{ vente.quantite }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(vente.date_vente) }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editVente(vente)" class="text-blue-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
              <span>Modifier</span>
            </button>
            <button @click="deleteVente(vente.id)" class="text-red-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>Supprimer</span>
            </button>
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

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Vente' : 'Ajouter Vente' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Produit</label>
            <select v-model="form.produit" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option v-for="produit in produits" :key="produit.id" :value="produit.id">{{ produit.nom }}</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Quantité</label>
            <input v-model.number="form.quantite" type="number" min="1" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Date de Vente</label>
            <input v-model="form.date_vente" type="date" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100">Annuler</button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">{{ isEditing ?
              'Enregistrer' : 'Ajouter' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getHistoriqueVentes, createHistoriqueVente, updateHistoriqueVente, deleteHistoriqueVente, getProduits } from '@/api/api.js'

export default {
  name: 'HistoriqueVentesPage',
  data() {
    return {
      ventes: [],
      produits: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        produit: null,
        quantite: 1,
        date_vente: ''
      }
    }
  },
  computed: {
    filteredVentes() {
      if (!this.searchQuery) return this.ventes
      return this.ventes.filter(v =>
        v.produit_nom.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages() {
      return Math.ceil(this.filteredVentes.length / this.pageSize)
    },
    paginatedVentes() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredVentes.slice(start, start + this.pageSize)
    }
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric' })
    },

    async fetchVentes() {
      try {
        const response = await getHistoriqueVentes()
        this.ventes = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des ventes:', error)
      }
    },
    async fetchProduits() {
      try {
        const response = await getProduits()
        this.produits = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error)
      }
    },
    openModal() {
      this.resetForm()
      this.showModal = true
      this.isEditing = false
    },
    closeModal() {
      this.showModal = false
    },
    resetForm() {
      this.form = {
        id: null,
        produit: null,
        quantite: 1,
        date_vente: ''
      }
    },
    editVente(vente) {
      this.form = {
        id: vente.id,
        produit: vente.produit,
        quantite: vente.quantite,
        date_vente: vente.date_vente ? vente.date_vente.substr(0, 10) : ''
      }
      this.showModal = true
      this.isEditing = true
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          await updateHistoriqueVente(this.form.id, this.form)
        } else {
          await createHistoriqueVente(this.form)
        }
        this.closeModal()
        this.fetchVentes()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de la vente:', error)
      }
    },
    async deleteVente(id) {
      if (confirm('Voulez-vous vraiment supprimer cette vente ?')) {
        try {
          await deleteHistoriqueVente(id)
          this.fetchVentes()
        } catch (error) {
          console.error('Erreur lors de la suppression de la vente:', error)
        }
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  },
  mounted() {
    this.fetchVentes()
    this.fetchProduits()
  }
}
</script>
