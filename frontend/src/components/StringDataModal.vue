<script setup lang="ts">
import ChatMessage from '@/components/ChatMessage.vue';
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions';
import { inject, onMounted, ref, type Ref } from 'vue';

const dialogRef = inject<Ref<DynamicDialogInstance>>('dialogRef');

let stringData = ref('');

onMounted(() => {
  const props = dialogRef?.value.data;

  console.log(props.stringData);
  stringData.value = props?.stringData;
});
</script>

<template>
  <ChatMessage
    v-if="stringData"
    :is-sent="false"
    :message="stringData"
    :full-width="true"
  ></ChatMessage>
</template>
