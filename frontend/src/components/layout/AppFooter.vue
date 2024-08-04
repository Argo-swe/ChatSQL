<script setup lang="ts">
// External libraries
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// Reference to the application version.
const version = ref(import.meta.env.VITE_VERSION ?? null);
</script>

<template>
  <div class="layout-footer w-full">
    <div class="logo">
      <app-logo path="icons/argo_trasparente.svg" height="40"></app-logo>
    </div>
    <p class="copyright">
      <strong v-if="version"> v{{ version }} </strong>
      <span>© {{ new Date().getFullYear() }} {{ t('footer.copyright.title') }}</span>
      <span>{{ t('footer.copyright.section') }}</span>
    </p>
  </div>
</template>
