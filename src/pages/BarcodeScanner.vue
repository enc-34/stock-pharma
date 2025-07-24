<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Scanner un produit</h2>
    <div id="scanner" class="border border-gray-300 rounded w-80 h-64 mx-auto"></div>

    <p v-if="code" class="mt-4 text-green-600 font-semibold">
      Code détecté : {{ code }}
    </p>
    <button v-if="code" @click="rechercherProduit" class="mt-2 bg-blue-600 text-white px-4 py-2 rounded">
      Rechercher le produit
    </button>

    <div v-if="produit" class="mt-4 p-2 border border-gray-200 rounded bg-gray-100">
      <h3 class="font-bold">Produit : {{ produit.nom }}</h3>
      <p>Stock actuel : {{ produit.stock }}</p>
      <button @click="mettreAJourStock" class="mt-2 bg-green-600 text-white px-4 py-2 rounded">
        + Ajouter 1 au stock
      </button>
    </div>
  </div>
</template>

<script>
import Quagga from 'quagga'
import axios from 'axios'

export default {
  data() {
    return {
      code: null,
      produit: null
    }
  },
  mounted() {
    Quagga.init({
      inputStream: {
        type: "LiveStream",
        constraints: { facingMode: "environment" },
        target: document.querySelector('#scanner')
      },
      decoder: { readers: ["ean_reader", "code_128_reader"] }
    }, (err) => {
      if (err) {
        console.log(err);
        return;
      }
      Quagga.start();
    });

    Quagga.onDetected(this.onDetected);
  },
  methods: {
    onDetected(result) {
      this.code = result.codeResult.code;
      Quagga.stop(); // Stop après détection
    },
    async rechercherProduit() {
      try {
        const res = await axios.get(`/api/produits/scan?barcode=${this.code}`);
        this.produit = res.data;
      } catch {
        alert("Produit non trouvé !");
      }
    },
    async mettreAJourStock() {
      try {
        const res = await axios.patch(`/api/produits/${this.produit.id}/`, {
          stock: this.produit.stock + 1
        });
        this.produit = res.data;
        alert("Stock mis à jour !");
      } catch (e) {
        console.log(e);
      }
    }
  },
  beforeUnmount() {
    Quagga.stop();
  }
}
</script>
<style lang="css" scoped>
#scanner {
  width: 320px;
  height: 240px;
  margin: 0 auto;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #000;
}
</style>
