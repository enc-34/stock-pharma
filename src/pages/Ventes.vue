<template>
  <div class="rounded-lg p-6">
    <h1 class="text-2xl font-bold mb-4">Gestion des Ventes</h1>

    <form @submit.prevent="submitVente" class="mb-6 max-w-md">
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Produit</label>
        <select v-model="form.produit" required class="w-full border border-gray-300 rounded px-3 py-2">
          <option value="" disabled>Choisissez un produit</option>
          <option v-for="produit in produits" :key="produit.id" :value="produit.id">
            {{ produit.nom }} (Stock: {{ produit.stock }})
          </option>
        </select>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Quantité vendue</label>
        <input v-model.number="form.quantite" type="number" min="1" required
          class="w-full border border-gray-300 rounded px-3 py-2" />
      </div>
      <div v-if="errorMessage" class="mb-4 text-red-600">{{ errorMessage }}</div>
      <div class="flex space-x-2">
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Enregistrer la
          vente</button>
        <button type="button" @click="cancelVente" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
          Annuler
        </button>
      </div>
    </form>

    <h2 class="text-xl font-bold mb-2">Historique des Ventes</h2>
    <table class="w-full border-separate border-spacing-2 border border-green-400 dark:border-gray-700">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Produit</th>
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Quantité</th>
          <th class="border border-gray-300 dark:border-gray-600 px-3 py-2">Date de vente</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="vente in ventes" :key="vente.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">{{ vente.produit_nom }}</td>
          <td class="py-2 px-4 border-b">{{ vente.quantite }}</td>
          <td class="py-2 px-4 border-b">{{ formatDate(vente.date_vente) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VentesPage',
  data() {
    return {
      produits: [],
      ventes: [],
      form: {
        produit: '',
        quantite: 1
      },
      errorMessage: ''
    }
  },
  methods: {
    async fetchProduits() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/produits/')
        this.produits = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des produits:', error)
      }
    },
    async fetchVentes() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/ventes/')
        this.ventes = response.data
      } catch (error) {
        console.error('Erreur lors du chargement des ventes:', error)
      }
    },
    async submitVente() {
      this.errorMessage = ''
      if (!this.form.produit || this.form.quantite <= 0) {
        this.errorMessage = 'Veuillez sélectionner un produit et saisir une quantité valide.'
        return
      }
      try {
        await axios.post('http://127.0.0.1:8000/api/ventes/enregistrer_vente/', {
          produit: this.form.produit,
          quantite: this.form.quantite
        })
        this.form.produit = ''
        this.form.quantite = 1
        this.fetchVentes()
        this.fetchProduits()
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error
        } else {
          this.errorMessage = 'Erreur lors de l\'enregistrement de la vente.'
        }
        console.error('Erreur lors de l\'enregistrement de la vente:', error)
      }
    },
    cancelVente() {
      this.form.produit = ''
      this.form.quantite = 1
      this.errorMessage = ''
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
  },
  mounted() {
    this.fetchProduits()
    this.fetchVentes()
  }
}
</script>

<style scoped></style>
