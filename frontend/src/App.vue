<script setup lang="ts">
import Header from './components/Header.vue';
import OpenAPIClientAxios from 'openapi-client-axios';
import { ref } from 'vue';

const api = new OpenAPIClientAxios({ definition: 'http://localhost:5000/swagger.json' }); // FLASK
api.init();

const generatedPrompt = ref('');

async function button() {
  const client = await api.getClient();
  const res = await client.get_generate_prompt(); // FLASK
  console.log('Pet created', res.data);
  generatedPrompt.value = res.data.data;
}
</script>

<template>
  <router-view />
</template>

<style scoped></style>
