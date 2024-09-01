<script setup lang="ts">
// External libraries
import ConfirmDialog from 'primevue/confirmdialog';
import DynamicDialog from 'primevue/dynamicdialog';
</script>

<template>
  <router-view />
  <ConfirmDialog data-testid="confirm-dialog"></ConfirmDialog>
  <DynamicDialog />
</template>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
