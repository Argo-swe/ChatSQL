<script setup lang="ts">
import Header from './components/Header.vue';
import { getApiClient } from './services/api-client';

async function button() {
  const client = await getApiClient();
  // esempio di generazione prompt
  const resPrompt = await client.generatePrompt("prova");
  const prompt = resPrompt.data.data;

  // esempio di contenuto del file con id 1
  const resJsonFileContent = await client.getDictionaryFile(1)
  const fileContent = JSON.stringify(resJsonFileContent.data);
}
</script>

<template>
  <router-view />
</template>

<style scoped></style>
