<template>
  <div class="rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Fournisseurs</h1>
      <input v-model="searchQuery" type="text" placeholder="Rechercher un fournisseur..."
        class="border border-gray-300 rounded px-3 py-2 mr-4" />
      <button @click="openModal()"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
          stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <span>Ajouter Fournisseur</span>
      </button>
    </div>

    <table class="border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600">Nom</th>
          <th class="border border-gray-300 dark:border-gray-600">Contact</th>
          <th class="border border-gray-300 dark:border-gray-600">Email</th>
          <th class="border border-gray-300 dark:border-gray-600">Adresse</th>
          <th class="border border-gray-300 dark:border-gray-600">Fiabilité</th>
          <th class="border border-gray-300 dark:border-gray-600">Délai moyen livraison (jours)</th>
          <th class="border border-gray-300 dark:border-gray-600">Classement</th>
          <th class="border border-gray-300 dark:border-gray-600">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="fournisseur in paginatedFournisseurs" :key="fournisseur.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ fournisseur.nom }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.contact }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.email }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.adresse }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.fiabilite }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.delai_moyen_livraison }}</td>
          <td class="py-2 px-4 border-b">{{ fournisseur.classement }}</td>
          <td class="py-2 px-4 border-b space-x-2">
            <button @click="editFournisseur(fournisseur)"
              class="text-blue-600 hover:underline flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M15.232 5.232l3.536 3.536M9 11l6-6 3 3-6 6H9v-3z" />
              </svg>
              <span>Modifier</span>
            </button>
            <button @click="deleteFournisseur(fournisseur.id)"
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
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Modifier Fournisseur' : 'Ajouter Fournisseur' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label class="block mb-1">Nom</label>
            <input v-model="form.nom" type="text" required class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Contact</label>
            <input v-model="form.contact" type="text" class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Email</label>
            <input v-model="form.email" type="email" class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Adresse</label>
            <textarea v-model="form.adresse" class="w-full border border-gray-300 rounded px-3 py-2"></textarea>
          </div>
          <div class="mb-4">
            <label class="block mb-1">Fiabilité</label>
            <input v-model.number="form.fiabilite" type="number" min="1" max="10" step="0.1"
              class="w-full border border-gray-300 rounded px-3 py-2" />
          </div>
          <div class="mb-4">
            <label class="block mb-1">Délai moyen livraison (jours)</label>
            <input v-model.number="form.delai_moyen_livraison" type="number" min="0"
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
import { getFournisseurs, createFournisseur, updateFournisseur, deleteFournisseur } from '@/api/api.js'

export default {
  name: 'FournisseursPage',
  data() {
    return {
      fournisseurs: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 5,
      showModal: false,
      isEditing: false,
      form: {
        id: null,
        nom: '',
        contact: '',
        email: '',
        adresse: '',
        fiabilite: 5.0,
        delai_moyen_livraison: 0
      }
    }
  },
  computed: {
    filteredFournisseurs() {
      if (!this.searchQuery) return this.fournisseurs
      return this.fournisseurs.filter(fourn =>
        fourn.nom.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages() {
      return Math.ceil(this.filteredFournisseurs.length / this.pageSize)
    },
    paginatedFournisseurs() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredFournisseurs.slice(start, start + this.pageSize)
    }
  },
  methods: {
    async fetchFournisseurs() {
      try {
        const response = await getFournisseurs()
        this.fournisseurs = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des fournisseurs:', error)
      }
    },
    async detectCountry() {
      if (!navigator.geolocation) {
        console.warn('Géolocalisation non supportée par ce navigateur.')
        return
      }
      navigator.geolocation.getCurrentPosition(async position => {
        const { latitude, longitude } = position.coords
        try {
          const response = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=fr`)
          const data = await response.json()
          if (data && data.countryName) {
            this.form.contact = data.countryName
          }
        } catch (error) {
          console.error('Erreur lors de la détection du pays:', error)
        }
      }, error => {
        console.warn('Erreur de géolocalisation:', error.message)
      })
    },
    async openModal() {
      this.resetForm()
      await this.detectCountry()
      this.showModal = true
      this.isEditing = false
    },
    closeModal() {
      this.showModal = false
    },
    resetForm() {
      this.form = { id: null, nom: '', contact: '', email: '', adresse: '', fiabilite: 5.0, delai_moyen_livraison: 0 }
    },
    editFournisseur(fournisseur) {
      this.form = { ...fournisseur }
      this.showModal = true
      this.isEditing = true
    },
    async submitForm() {
      try {
        if (this.isEditing) {
          await updateFournisseur(this.form.id, this.form)
        } else {
          await createFournisseur(this.form)
        }
        this.closeModal()
        this.fetchFournisseurs()
      } catch (error) {
        console.error('Erreur lors de la sauvegarde du fournisseur:', error)
      }
    },
    async deleteFournisseur(id) {
      if (confirm('Voulez-vous vraiment supprimer ce fournisseur ?')) {
        try {
          await deleteFournisseur(id)
          this.fetchFournisseurs()
        } catch (error) {
          console.error('Erreur lors de la suppression du fournisseur:', error)
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
    this.fetchFournisseurs()
  }
}
</script>
