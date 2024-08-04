<script setup lang="ts">
// External libraries
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useLayout } from '@/composables/layout';

// Child Components
import AppFooter from './AppFooter.vue';
import AppMenu from './AppMenu.vue';

const { onMenuToggle } = useLayout();
const { t } = useI18n();
</script>

<template>
  <PgButton
    id="close-menu-sidebar"
    icon="pi pi-times"
    severity="contrast"
    outlined
    :aria-label="t('general.menu.closeMainNavMenu')"
    @click="onMenuToggle()"
  />
  <div class="flex flex-column justify-content-between flex-wrap h-full">
    <div class="flex m-2">
      <app-menu></app-menu>
    </div>
    <div class="flex m-2">
      <app-footer></app-footer>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#close-menu-sidebar {
  display: none;
}

@media (max-width: 991px) {
  #close-menu-sidebar {
    display: block;
    position: absolute;
    top: 0;
    right: 0;
  }
}
</style>
