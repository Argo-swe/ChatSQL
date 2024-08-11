<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import AuthService from '@/services/auth.service';
import AppMenuItem from './AppMenuItem.vue';

const { t } = useI18n();

const USER_MENU = [
  {
    items: [{ label: computed(() => t('text.Chat')), icon: 'pi pi-fw pi-comments', to: '/chat' }]
  }
];

const TECHNICIAN_MENU = [
  {
    items: [{ label: computed(() => t('text.Chat')), icon: 'pi pi-fw pi-comments', to: '/chat' }]
  },
  {
    label: computed(() => t('general.menu.technicianFunctionalities')),
    items: [
      {
        label: computed(() => t('dictionary.title', 2)),
        icon: 'pi pi-fw pi-database',
        to: '/dictionary'
      }
      // { label: computed(() => t('text.Debug')), icon: 'pi pi-fw pi-eye', to: '/debug' }
    ]
  }
];

let model = ref<any>(AuthService.isLogged() ? TECHNICIAN_MENU : USER_MENU);

onMounted(() => {
  window.addEventListener('token-localstorage-changed', () => {
    model.value = AuthService.isLogged() ? TECHNICIAN_MENU : USER_MENU;
  });
});
</script>

<template>
  <ul class="layout-menu">
    <template v-for="(item, i) in model" :key="item">
      <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
      <li v-if="item.separator" class="menu-separator"></li>
    </template>
  </ul>
</template>
