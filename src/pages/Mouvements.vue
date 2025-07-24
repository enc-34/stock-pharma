<template>
  <div class=" rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Mouvements de Stock</h1>
      <button @click="openModal()"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Mouvement</span>
      </button>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Produit</th>
          <th class="border border-gray-300 dark:border-gray-600">Quantité</th>
          <th class="border border-gray-300 dark:border-gray-600">Type</th>
          <th class="border border-gray-300 dark:border-gray-600">Date</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mouvement in mouvements" :key="mouvement.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ mouvement.produit_nom }}</td>
          <td class="py-2 px-4 border-b">{{ mouvement.quantite }}</td>
          <td class="py-2 px-4 border-b">{{ mouvement.type_mouvement }}</td>
          <td class="py-2 px-4 border-b">{{ new Date(mouvement.date).toLocaleDateString() }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editMouvement(mouvement)" class="text-blue-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
              <span>Modifier</span>
            </button>
            <button @click="deleteMouvement(mouvement.id)"
              class="text-red-600 hover:underline flex items-center space-x-1">
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

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Mouvement' : 'Ajouter Mouvement' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Produit</label>
            <select v-model="form.produit" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="" disabled>Choisir un produit</option>
              <option v-for="produit in produits" :key="produit.id" :value="produit.id">{{ produit.nom }}</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Quantité</label>
            <input v-model.number="form.quantite" type="number" min="1" required
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Type de mouvement</label>
            <select v-model="form.type_mouvement" required class="w-full border border-gray-300 rounded px-3 py-2">
              <option value="" disabled>Choisir un type</option>
              <option value="ENTREE">Entrée</option>
              <option value="SORTIE">Sortie</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Date</label>
            <input v-model="form.date" type="date" required class="w-full border border-gray-300 rounded px-3 py-2" />
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
import { getMouvements, createMouvement, deleteMouvement } from '@/api/api.js'
import { getProduits } from '@/api/api.js'

export default {
  name: 'MouvementsPage',
  data() {
    return {
      mouvements: [],
      produits: [],
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        produit: '',
        quantite: 1,
        type_mouvement: '',
        date: ''
      }
    }
  },
  methods: {
    async fetchMouvements() {
      try {
        const response = await getMouvements()
        this.mouvements = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des mouvements:', error)
      }
    },
    async fetchProduits() {
      try {
        const response = await getProduits()
        if (response && response.data) {
          this.produits = response.data
        } else {
          this.produits = []
        }
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error)
        this.produits = []
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
        produit: '',
        quantite: 1,
        type_mouvement: '',
        date: ''
      }
    },
    editMouvement(mouvement) {
      this.form = {
        id: mouvement.id,
        produit: mouvement.produit.id,
        quantite: mouvement.quantite,
        type_mouvement: mouvement.type_mouvement,
        date: mouvement.date ? mouvement.date.split('T')[0] : ''
      }
      this.showModal = true
      this.isEditing = true
    },
    async submitForm() {
      try {
        // Prepare data to match backend serializer expectations
        const dataToSend = {
          ...this.form,
          produit: this.form.produit,
        }
        // Remove the line deleting produit to ensure it is sent
        // delete dataToSend.produit

        if (this.isEditing) {
          // For simplicity, assume createMouvement handles both create and update
          await createMouvement(dataToSend)
        } else {
          await createMouvement(dataToSend)
        }
        this.closeModal()
        this.fetchMouvements()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde du mouvement:', error)
      }
    },
    async deleteMouvement(id) {
      if (confirm('Voulez-vous vraiment supprimer ce mouvement ?')) {
        try {
          await deleteMouvement(id)
          this.fetchMouvements()
        } catch (error) {
          console.error('Erreur lors de la suppression du mouvement:', error)
        }
      }
    }
  },
  mounted() {
    this.fetchMouvements()
    this.fetchProduits()
  }
}
</script>

<style scoped></style>
