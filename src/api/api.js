import axios from 'axios'
import { authHeader } from './auth'

const API_BASE = 'http://127.0.0.1:8000/api/'

function api() {
  return axios.create({
    baseURL: API_BASE,
    headers: authHeader(),
  })
}

// PRODUITS
export function getProduits() {
  return api().get('produits/')
}

export function createProduit(data) {
  return api().post('produits/', data)
}

export function updateProduit(id, data) {
  return api().put(`produits/${id}/`, data)
}

export function deleteProduit(id) {
  return api().delete(`produits/${id}/`)
}

// CATEGORIES
export function getCategories() {
  return api().get('categories/')
}

export function createCategorie(data) {
  return api().post('categories/', data)
}

export function deleteCategorie(id) {
  return api().delete(`categories/${id}/`)
}

// FOURNISSEURS
export function getFournisseurs() {
  return api().get('fournisseurs/')
}

export function createFournisseur(data) {
  return api().post('fournisseurs/', data)
}

export function updateFournisseur(id, data) {
  return api().put(`fournisseurs/${id}/`, data)
}

export function deleteFournisseur(id) {
  return api().delete(`fournisseurs/${id}/`)
}

// COMMANDES FOURNISSEURS
export function getCommandesFournisseurs() {
  return api().get('commandes-fournisseurs/')
}

export function createCommandeFournisseur(data) {
  return api().post('commandes-fournisseurs/', data)
}

export function updateCommandeFournisseur(id, data) {
  return api().put(`commandes-fournisseurs/${id}/`, data)
}

export function deleteCommandeFournisseur(id) {
  return api().delete(`commandes-fournisseurs/${id}/`)
}

// MOUVEMENTS
export function getMouvements() {
  return api().get('mouvements/')
}

export function createMouvement(data) {
  return api().post('mouvements/', data)
}

export function deleteMouvement(id) {
  return api().delete(`mouvements/${id}/`)
}

// DASHBOARD
export function getDashboardStats() {
  return api().get('dashboard/stats/')
}

// HISTORIQUE VENTES
export function getHistoriqueVentes() {
  return api().get('ventes/')
}

export function createHistoriqueVente(data) {
  return api().post('ventes/', data)
}

export function updateHistoriqueVente(id, data) {
  return api().put(`ventes/${id}/`, data)
}

export function deleteHistoriqueVente(id) {
  return api().delete(`ventes/${id}/`)
}

// APPROVISIONNEMENTS AUTO
export function getApprovisionnementsAuto() {
  return api().get('approvisionnements-auto/')
}

export function createApprovisionnementAuto(data) {
  return api().post('approvisionnements-auto/', data)
}

export function updateApprovisionnementAuto(id, data) {
  return api().put(`approvisionnements-auto/${id}/`, data)
}

export function deleteApprovisionnementAuto(id) {
  return api().delete(`approvisionnements-auto/${id}/`)
}

export function genererCommandeApprovisionnement(id) {
  return api().post(`approvisionnements-auto/${id}/generer-commande/`)
}
