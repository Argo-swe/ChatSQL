<script setup lang="ts">
import Header from './components/Header.vue';
import { getApiClient } from './services/api-client';

async function button() {
  const client = await getApiClient();
  // esempio di generazione prompt
  const resPrompt = await client.generate_prompt_api_prompt__get("prova");
  const prompt = resPrompt.data.data;

  // esempio di contenuto del file con id 1
  const resJsonFileContent = await client.get_dictionary_file_api_dictionary__id__file_get(1)
  const fileContent = JSON.stringify(resJsonFileContent.data);
}
</script>

<template>
  <Header />
  <RouterView />
</template>
