<template>
  <div class="p-6 space-y-8">
    <!-- HEADER STATS -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white shadow rounded-xl p-4 flex items-center space-x-4">
        <div class="bg-blue-100 p-2 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 6h18M3 14h18M3 18h18" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold">{{ dashboardStats.total_produits }}</div>
          <p class="text-gray-500 text-sm">Produits</p>
        </div>
      </div>

      <div class="bg-white shadow rounded-xl p-4 flex items-center space-x-4">
        <div class="bg-green-100 p-2 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold">{{ dashboardStats.total_stock }}</div>
          <p class="text-gray-500 text-sm">Stock Actuel</p>
        </div>
      </div>

      <div class="bg-white shadow rounded-xl p-4 flex items-center space-x-4">
        <div class="bg-purple-100 p-2 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold">{{ dashboardStats.total_categories }}</div>
          <p class="text-gray-500 text-sm">Catégories</p>
        </div>
      </div>
    </section>

    <!-- ALERTES -->
    <section>
      <h2 class="text-xl font-bold mb-4">Alertes</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded shadow">
          <h3 class="font-semibold mb-2 text-red-700">Produits périmés</h3>
          <ul>
            <li v-for="produit in alertesExpiration" :key="produit.id">
              {{ produit.nom }} - Expiré le {{ produit.date_expiration }}
            </li>
            <li v-if="alertesExpiration.length === 0">Aucun produit périmé</li>
          </ul>
        </div>
        <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded shadow">
          <h3 class="font-semibold mb-2 text-yellow-700">Stock faible</h3>
          <ul v-if="alertesStockBas.length > 0">
            <li v-for="produit in alertesStockBas" :key="produit.id">
              {{ produit.nom }} - Stock: {{ produit.stock }}
            </li>
          </ul>
          <p v-else>Aucun produit en rupture</p>
        </div>
      </div>
    </section>

    <!-- GRAPHIQUES -->
    <section>
      <h2 class="text-xl font-bold mb-4">Graphiques</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Stock</h3>
          <canvas id="stockChart"></canvas>
        </div>
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Ventes (Top Produits)</h3>
          <canvas id="salesChart"></canvas>
        </div>
      </div>
    </section>

    <!-- TOP PRODUITS -->
    <section>
      <h2 class="text-xl font-bold mb-4">Top 5 Produits Vendus</h2>
      <table class="w-full border-collapse bg-white rounded-xl shadow overflow-hidden">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 text-left">Produit</th>
            <th class="px-4 py-2 text-left">Ventes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="produit in topProduits" :key="produit.id" class="border-t hover:bg-gray-50">
            <td class="px-4 py-2">{{ produit.nom }}</td>
            <td class="px-4 py-2">{{ produit.ventes }}</td>
          </tr>
          <tr v-if="topProduits.length === 0">
            <td colspan="2" class="px-4 py-2 text-center">Aucun produit vendu</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import { getDashboardStats } from '@/api/api.js'

export default {
  name: 'DashboardPage',
  setup() {
    const alertesExpiration = ref([])
    const alertesStockBas = ref([])
    const dashboardStats = ref({
      total_produits: 0,
      total_stock: 0,
      total_categories: 0,
    })
    const topProduits = ref([])

    let stockChartInstance = null
    let salesChartInstance = null

    const fetchAlertes = async () => {
      try {
        const resExp = await fetch('http://127.0.0.1:8000/api/alertes/expiration/')
        alertesExpiration.value = await resExp.json()
        const resStock = await fetch('http://127.0.0.1:8000/api/alertes/stock_bas/')
        alertesStockBas.value = await resStock.json()
      } catch (error) {
        console.error('Erreur alertes:', error)
      }
    }

    const fetchDashboardStats = async () => {
      try {
        const response = await getDashboardStats()
        dashboardStats.value = response.data
      } catch (error) {
        console.error('Erreur stats:', error)
      }
    }

    const fetchTopProduits = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/dashboard/top5_produits/')
        topProduits.value = await response.json()
      } catch (error) {
        console.error('Erreur top produits:', error)
      }
    }

    const renderCharts = () => {
      if (stockChartInstance) stockChartInstance.destroy()
      if (salesChartInstance) salesChartInstance.destroy()

      const ctxStock = document.getElementById('stockChart').getContext('2d')
      stockChartInstance = new Chart(ctxStock, {
        type: 'bar',
        data: {
          labels: ['Stock actuel'],
          datasets: [{
            data: [dashboardStats.value.total_stock],
            backgroundColor: 'rgba(34,197,94,0.7)',
          }],
        },
      })

      const ctxSales = document.getElementById('salesChart').getContext('2d')
      salesChartInstance = new Chart(ctxSales, {
        type: 'bar',
        data: {
          labels: topProduits.value.map(p => p.nom),
          datasets: [{
            data: topProduits.value.map(p => p.ventes),
            backgroundColor: 'rgba(59,130,246,0.7)',
          }],
        },
      })
    }

    onMounted(async () => {
      await fetchAlertes()
      await fetchDashboardStats()
      await fetchTopProduits()
      renderCharts()
    })

    return { alertesExpiration, alertesStockBas, dashboardStats, topProduits }
  },
}
</script>
