<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppLogo'
});
</script>

<template>
  <img src="../../public/icons/argo_icona.svg" alt="Logo" height="40" class="logo" />
</template>

<style scoped>
.logo {
  cursor: pointer;
}
</style>
