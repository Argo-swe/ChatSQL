<script setup lang="ts">
// External libraries
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions';
import { inject, onMounted, ref, type Ref } from 'vue';

// Child Components
import DebugMessage from './DebugMessage.vue';

const dialogRef = inject<Ref<DynamicDialogInstance>>('dialogRef');
let stringData = ref('');

onMounted(() => {
  const props = dialogRef?.value.data;
  stringData.value = props?.stringData;
});
</script>

<template>
  <DebugMessage v-if="stringData" :message="stringData"></DebugMessage>
</template>
