<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Commandes Fournisseurs</h1>
      <input v-model="searchQuery" type="text" placeholder="Rechercher une commande..."
        class="border border-gray-300 rounded px-3 py-2 mr-4" />
      <button @click="openAddModal"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Commande</span>
      </button>
    </div>

    <!-- Modal for adding a new commande -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Ajouter une nouvelle commande</h2>
        <form @submit.prevent="submitAddCommande">
          <div class="mb-4">
            <label class="block mb-1">Référence</label>
            <input v-model="newCommande.reference" type="text" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Fournisseur</label>
            <select v-model="newCommande.fournisseur" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option v-for="f in fournisseurs" :key="f.id" :value="f.id">{{ f.nom }}</option>
            </select>

          </div>
          <div class="mb-4">
            <label class="block mb-1">Date Commande</label>
            <input v-model="newCommande.date_commande" type="date" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Date Livraison</label>
            <input v-model="newCommande.date_livraison" type="date" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Statut</label>
            <select v-model="newCommande.statut" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="EN_ATTENTE">En attente</option>
              <option value="EN_COURS">En cours</option>
              <option value="LIVREE">Livrée</option>
              <option value="ANNULEE">Annulée</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeAddModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100">Annuler</button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Ajouter</button>
          </div>
        </form>
      </div>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Référence</th>
          <th class="border border-gray-300 dark:border-gray-600">Fournisseur</th>
          <th class="border border-gray-300 dark:border-gray-600">Date Commande</th>
          <th class="border border-gray-300 dark:border-gray-600">Date Livraison</th>
          <th class="border border-gray-300 dark:border-gray-600">Statut</th>
          <th class="border border-gray-300 dark:border-gray-600">En Retard</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="commande in paginatedCommandes" :key="commande.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ commande.reference }}</td>
          <td class="py-2 px-4 border-b">{{ commande.fournisseur }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(commande.date_commande) }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(commande.date_livraison) }}</td>
          <td class="py-2 px-4 border-b">{{ commande.statut }}</td>
          <td class="py-2 px-4 border-b">{{ isEnRetard(commande) ? 'Oui' : 'Non' }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="downloadPDF(commande)" class="text-green-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
              <span>Télécharger PDF</span>
            </button>
            <button @click="changeStatus(commande)" class="text-blue-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
              <span>Changer Statut</span>
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

    <!-- Modal for changing status -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Changer le statut de la commande</h2>
        <form @submit.prevent="submitStatusChange">
          <div class="mb-4">
            <label class="block mb-1">Statut</label>
            <select v-model="statusForm.statut" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="EN_ATTENTE">En attente</option>
              <option value="EN_COURS">En cours</option>
              <option value="LIVREE">Livrée</option>
              <option value="ANNULEE">Annulée</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeStatusModal"
              class="px-4 py-2 rounded border border-gray-300 hover:bg-gray-100">Annuler</button>
            <button type="submit"
              class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Enregistrer</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { getCommandesFournisseurs, updateCommandeFournisseur } from '@/api/api.js'
import axios from 'axios'


export default {
  name: 'CommandesFournisseursPage',
  data() {
    return {
      commandes: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      showStatusModal: false,
      statusForm: {
        id: null,
        statut: 'EN_ATTENTE'
      },
      showAddModal: false,
      newCommande: {
        reference: '',
        fournisseur: [],
        date_commande: '',
        date_livraison: '',
        statut: 'EN_ATTENTE'
      }
    }
  },
  computed: {
    filteredCommandes() {
      if (!this.searchQuery) return this.commandes
      return this.commandes.filter(cmd =>
        cmd.reference.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        cmd.fournisseur.nom.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages() {
      return Math.ceil(this.filteredCommandes.length / this.pageSize)
    },
    paginatedCommandes() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredCommandes.slice(start, start + this.pageSize)
    }
  },
  methods: {
    async fetchCommandes() {
      try {
        const response = await getCommandesFournisseurs()
        this.commandes = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des commandes:', error)
      }
    },
    async fetchFournisseurs() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/fournisseurs/')
        this.fournisseurs = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des fournisseurs:', error)
      }
    },
    openAddModal() {
      this.showAddModal = true
    },
    closeAddModal() {
      this.showAddModal = false
      this.resetNewCommande()
    },
    resetNewCommande() {
      this.newCommande = {
        reference: '',
        fournisseur: '',
        date_commande: '',
        date_livraison: '',
        statut: 'EN_ATTENTE'
      }
    },
    async submitAddCommande() {
      try {
        const payload = {
          reference: this.newCommande.reference,
          fournisseur: this.newCommande.fournisseur,
          date_commande: this.newCommande.date_commande,
          date_livraison: this.newCommande.date_livraison,
          statut: this.newCommande.statut
        }

        const response = await axios.post('http://127.0.0.1:8000/api/commandes-fournisseurs/', payload)
        this.commandes.push(response.data)
        this.closeAddModal()
      } catch (error) {
        console.error('Erreur lors de l\'ajout de la commande:', error)
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString()
    },
    downloadPDF(commande) {
      window.open(`http://127.0.0.1:8000/api/commandes-fournisseurs/${commande.id}/pdf/`, '_blank')
    },
    changeStatus(commande) {
      this.statusForm.id = commande.id
      this.statusForm.statut = commande.statut
      this.showStatusModal = true
    },
    closeStatusModal() {
      this.showStatusModal = false
    },
    async submitStatusChange() {
      if (!confirm(`Voulez-vous vraiment changer le statut en ${this.statusForm.statut} ?`)) return
      try {
        await updateCommandeFournisseur(this.statusForm.id, { statut: this.statusForm.statut })
        this.showStatusModal = false
        this.fetchCommandes()
      } catch (error) {
        console.error('Erreur lors du changement de statut:', error)
      }
    },
    isEnRetard(commande) {
      return commande.statut !== 'LIVREE' && commande.date_livraison && new Date(commande.date_livraison) < new Date()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    }
  },
  mounted() {
    this.fetchCommandes()
    this.fetchFournisseurs()
  }
}
</script>
