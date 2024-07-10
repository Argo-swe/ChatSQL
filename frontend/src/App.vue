<script setup lang="ts">
import ConfirmDialog from 'primevue/confirmdialog';
import DynamicDialog from 'primevue/dynamicdialog';
</script>

<template>
  <router-view />
  <ConfirmDialog></ConfirmDialog>
  <DynamicDialog />
</template>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
