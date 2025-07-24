<template>
  <div class="flex min-h-screen flex-col">
    <Header />
    <div class="flex flex-1">
      <AppSidebar />
      <main class="flex-1 p-6 bg-gray-50">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import AppSidebar from '@/components/AppSidebar.vue'
</script>

<style scoped></style>
