<script setup>
import { useRoute } from 'vue-router'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import { computed } from 'vue'

const route = useRoute()

const isLoginPage = computed(() => route.path === '/login')
</script>

<template>
  <LayoutAuthenticated v-if="!isLoginPage">
    <router-view />
  </LayoutAuthenticated>
  <router-view v-else />
</template>
