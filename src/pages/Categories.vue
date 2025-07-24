<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Catégories</h1>
      <button @click="openModal()"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Catégorie</span>
      </button>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Nom</th>
          <th class="border border-gray-300 dark:border-gray-600">Description</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>

        </tr>
      </thead>
      <tbody>
        <tr v-for="categorie in categories" :key="categorie.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ categorie.nom }}</td>
          <td class="py-2 px-4 border-b">{{ categorie.description }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editCategorie(categorie)" class="text-blue-600 hover:underline flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
            </button>
            <button @click="deleteCategorie(categorie.id)" class="text-red-600 hover:underline flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Catégorie' : 'Ajouter Catégorie' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Nom</label>
            <input v-model="form.nom" type="text" required class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Description</label>
            <input v-model="form.description" type="text" required
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
import { getCategories, createCategorie, deleteCategorie } from '@/api/api.js'

export default {
  name: 'CategoriesPage',
  data() {
    return {
      categories: [],
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        nom: '',
        description: ''
      }
    }
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await getCategories()
        this.categories = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error)
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
        nom: '',
        description: '',
      }
    },
    editCategorie(categorie) {
      this.form = { ...categorie }
      this.showModal = true
      this.isEditing = true
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          // For simplicity, assume createCategorie handles both create and update
          await createCategorie(this.form)
        } else {
          await createCategorie(this.form)
        }
        this.closeModal()
        this.fetchCategories()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de la catégorie:', error)
      }
    },
    async deleteCategorie(id) {
      if (confirm('Voulez-vous vraiment supprimer cette catégorie ?')) {
        try {
          await deleteCategorie(id)
          this.fetchCategories()
        } catch (error) {
          console.error('Erreur lors de la suppression de la catégorie:', error)
        }
      }
    }
  },
  mounted() {
    this.fetchCategories()
  }
}
</script>

<style scoped></style>
