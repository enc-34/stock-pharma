<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Approvisionnements Automatiques</h1>
      <input v-model="searchQuery" type="text" placeholder="Rechercher un produit..."
        class="border border-gray-300 rounded px-3 py-2 mr-4" />
      <button @click="openModal()"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Approvisionnement</span>
      </button>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Produit</th>
          <th class="border border-gray-300 dark:border-gray-600">Quantité Suggérée</th>
          <th class="border border-gray-300 dark:border-gray-600">Date Proposition</th>
          <th class="border border-gray-300 dark:border-gray-600">Commande Générée</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appro in paginatedApprovisionnements" :key="appro.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ appro.produit_nom }}</td>
          <td class="py-2 px-4 border-b">{{ appro.quantite_suggeree }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(appro.date_proposition) }}</td>
          <td class="py-2 px-4 border-b">{{ appro.commande_generee ? 'Oui' : 'Non' }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editApprovisionnement(appro)"
              class="text-blue-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
              <span>Modifier</span>
            </button>
            <button @click="deleteApprovisionnement(appro.id)"
              class="text-red-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>Supprimer</span>
            </button>
            <button v-if="!appro.commande_generee" @click="genererCommande(appro.id)"
              class="text-green-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
              <span>Générer Commande</span>
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
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Approvisionnement' : 'Ajouter Approvisionnement' }}
        </h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Produit</label>
            <select v-model="form.produit" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option v-for="produit in produits" :key="produit.id" :value="produit.id">{{ produit.nom }}</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Quantité Suggérée</label>
            <input v-model.number="form.quantite_suggeree" type="number" min="1" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Date Proposition</label>
            <input v-model="form.date_proposition" type="date" required
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
import { getApprovisionnementsAuto, createApprovisionnementAuto, updateApprovisionnementAuto, deleteApprovisionnementAuto, genererCommandeApprovisionnement, getProduits } from '@/api/api.js'

export default {
  name: 'ApprovisionnementsAutoPage',
  data() {
    return {
      approvisionnements: [],
      produits: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        produit: null,
        quantite_suggeree: 1,
        date_proposition: ''
      }
    }
  },
  computed: {
    filteredApprovisionnements() {
      if (!this.searchQuery) return this.approvisionnements
      return this.approvisionnements.filter(appro =>
        appro.produit_nom.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages() {
      return Math.ceil(this.filteredApprovisionnements.length / this.pageSize)
    },
    paginatedApprovisionnements() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredApprovisionnements.slice(start, start + this.pageSize)
    }
  },
  methods: {
    async fetchApprovisionnements() {
      try {
        const response = await getApprovisionnementsAuto()
        this.approvisionnements = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des approvisionnements:', error)
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
      this.resetForm()
    },
    resetForm() {
      this.form = {
        id: null,
        produit: null,
        quantite_suggeree: 1,
        date_proposition: ''
      }
    },
    editApprovisionnement(appro) {
      this.form = {
        id: appro.id,
        produit: appro.produit,
        quantite_suggeree: appro.quantite_suggeree,
        date_proposition: appro.date_proposition ? appro.date_proposition.substr(0, 10) : ''
      }
      this.showModal = true
      this.isEditing = true
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          await updateApprovisionnementAuto(this.form.id, this.form)
        } else {
          await createApprovisionnementAuto(this.form)
        }
        this.closeModal()
        this.fetchApprovisionnements()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'approvisionnement:', error)
      }
    },
    async deleteApprovisionnement(id) {
      if (confirm('Voulez-vous vraiment supprimer cet approvisionnement ?')) {
        try {
          await deleteApprovisionnementAuto(id)
          this.fetchApprovisionnements()
        } catch (error) {
          console.error('Erreur lors de la suppression de l\'approvisionnement:', error)
        }
      }
    },
    async genererCommande(id) {
      try {
        await genererCommandeApprovisionnement(id)
        this.fetchApprovisionnements()
      } catch (error) {
        console.error('Erreur lors de la génération de la commande:', error)
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('fr-FR')
    }
  },
  mounted() {
    this.fetchApprovisionnements()
    this.fetchProduits()
  }
}
</script>
