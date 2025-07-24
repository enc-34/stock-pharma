<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4"><br><br>
      <h1 class="text-2xl font-bold">GESTION Produits</h1><br><br><br>
      <div class="flex space-x-2 items-center">
        <input v-model="searchQuery" type="text" placeholder="Rechercher un produit..."
          class="border border-gray-300 rounded px-3 py-2" />
        <button @click="openModal()" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Ajouter
          Produit</button>
        <button @click="exportCSV" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Exporter
          CSV</button>
        <button @click="downloadPDF" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">Télécharger
          PDF</button>
      </div>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Nom</th>
          <th class="border border-gray-300 dark:border-gray-600">Prix</th>
          <th class="border border-gray-300 dark:border-gray-600">Stock</th>
          <th class="border border-gray-300 dark:border-gray-600">Stock Min</th>
          <th class="border border-gray-300 dark:border-gray-600">Catégorie</th>
          <th class="border border-gray-300 dark:border-gray-600">Fournisseur</th>
          <th class="border border-gray-300 dark:border-gray-600">Date Expiration</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="produit in paginatedProduits" :key="produit.id" :class="{ 'bg-red-100': isExpired(produit) }"
          class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ produit.nom }}</td>
          <td class="py-2 px-4 border-b">{{ produit.prix }} FCFA</td>
          <td class="py-2 px-4 border-b">{{ produit.stock }}</td>
          <td class="py-2 px-4 border-b">{{ produit.stock_min }}</td>
          <td class="py-2 px-4 border-b">{{ produit.categorie_nom || '-' }}</td>
          <td class="py-2 px-4 border-b">{{ produit.fournisseur_nom || '-' }}</td>
          <td class="py-2 px-4 border-b">{{ produit.date_expiration || '-' }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editProduit(produit)" class="text-blue-600 hover:underline">Modifier</button>
            <button @click="deleteProduit(produit.id)" class="text-red-600 hover:underline">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Produit' : 'Ajouter Produit' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Nom</label>
            <input v-model="form.nom" type="text" required class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Prix (FCFA)</label>
            <input v-model.number="form.prix" type="number" min="0" step="0.01" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Stock</label>
            <input v-model.number="form.stock" type="number" min="0" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Date d'expiration</label>
            <input v-model="form.date_expiration" type="date" class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <!-- Add select inputs for categorie_id and fournisseur_id in the modal form -->
          <!-- This part should be added inside the form in the modal -->
          <div class="mb-4">
            <label class="block mb-1">Catégorie</label>
            <select v-model="form.categorie_id" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="" disabled>Choisissez une catégorie</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.nom }}</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Fournisseur</label>
            <select v-model="form.fournisseur_id" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="" disabled>Choisissez un fournisseur</option>
              <option v-for="fourn in fournisseurs" :key="fourn.id" :value="fourn.id">{{ fourn.nom }}</option>
            </select>
          </div>
          <div v-if="errorMessage" class="mb-4 text-red-600">
            {{ errorMessage }}
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
import { getProduits, createProduit, updateProduit, deleteProduit, getCategories, getFournisseurs } from '@/api/api.js'

export default {
  name: 'ProduitsPage',
  data() {
    return {
      produits: [],
      categories: [],
      fournisseurs: [],
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        nom: '',
        prix: 0,
        stock: 0,
        stock_min: 10,
        date_expiration: '',
        categorie_id: null,
        fournisseur_id: null
      },
      errorMessage: '',
      searchQuery: '',
      currentPage: 1,
      pageSize: 5
    }
  },
  computed: {
    filteredProduits() {
      if (!this.searchQuery) {
        return this.produits
      }
      const query = this.searchQuery.toLowerCase()
      return this.produits.filter(p =>
        p.nom.toLowerCase().includes(query)
      )
    },
    totalPages() {
      return Math.ceil(this.filteredProduits.length / this.pageSize)
    },
    paginatedProduits() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredProduits.slice(start, end)
    }
  },
  methods: {
    async fetchProduits() {
      try {
        const response = await getProduits()
        // Ajouter stock_min si absent dans les produits reçus
        this.produits = response.data.map(p => ({
          ...p,
          stock_min: p.stock_min !== undefined ? p.stock_min : 10
        }))
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error)
      }
    },
    async fetchCategories() {
      try {
        const response = await getCategories()
        this.categories = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error)
      }
    },
    async fetchFournisseurs() {
      try {
        const response = await getFournisseurs()
        this.fournisseurs = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des fournisseurs:', error)
      }
    },
    openModal() {
      this.resetForm()
      this.showModal = true
      this.isEditing = false
      this.errorMessage = ''
    },
    closeModal() {
      this.showModal = false
      this.errorMessage = ''
    },
    resetForm() {
      this.form = {
        id: null,
        nom: '',
        prix: 0,
        stock: 0,
        date_expiration: '',
        categorie_id: null,
        fournisseur_id: null
      }
      this.errorMessage = ''
    },
    editProduit(produit) {
      this.form = { ...produit }
      this.showModal = true
      this.isEditing = true
      this.errorMessage = ''
    },
    async submitForm() {
      try {
        // Format date_expiration to ISO string if not empty
        if (this.form.date_expiration) {
          this.form.date_expiration = new Date(this.form.date_expiration).toISOString().split('T')[0]
        } else {
          this.form.date_expiration = null
        }

        // Prepare data to send with correct keys for backend
        const dataToSend = {
          ...this.form,
          categorie: this.form.categorie_id ? Number(this.form.categorie_id) : null,
          fournisseur: this.form.fournisseur_id ? Number(this.form.fournisseur_id) : null
        }
        // Remove categorie_id and fournisseur_id from dataToSend
        delete dataToSend.categorie_id
        delete dataToSend.fournisseur_id

        if (this.isEditing) {
          await updateProduit(this.form.id, dataToSend)
        } else {
          await createProduit(dataToSend)
        }
        this.closeModal()
        this.fetchProduits()
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = JSON.stringify(error.response.data)
        } else {
          this.errorMessage = 'Erreur lors de la sauvegarde du produit.'
        }
        console.error('Erreur lors de la sauvegarde du produit:', error)
      }
    },
    async deleteProduit(id) {
      if (confirm('Voulez-vous vraiment supprimer ce produit ?')) {
        try {
          await deleteProduit(id)
          this.fetchProduits()
        } catch (error) {
          console.error('Erreur lors de la suppression du produit:', error)
        }
      }
    },
    exportCSV() {
      window.open('http://127.0.0.1:8000/api/export/produits/csv/', '_blank')
    },
    downloadPDF() {
      window.open('http://127.0.0.1:8000/api/export/produits/pdf/', '_blank')
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
    isExpired(produit) {
      if (!produit.date_expiration) return false
      const today = new Date()
      const expirationDate = new Date(produit.date_expiration)
      return expirationDate < today
    }
  },
  mounted() {
    this.fetchProduits()
    this.fetchCategories()
    this.fetchFournisseurs()
  }
}
</script>

<style scoped></style>
