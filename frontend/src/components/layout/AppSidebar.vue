<script setup lang="ts">
import AppMenu from './AppMenu.vue';
import AppFooter from './AppFooter.vue';
import { useLayout } from '@/components/layout/composables/layout';
const { onMenuToggle } = useLayout();

import { useI18n } from 'vue-i18n'
const { t } = useI18n();
</script>

<template>
    <Button id="close-menu-sidebar" icon="pi pi-times" severity="contrast" outlined :aria-label="t('general.menu.closeMainNavMenu')" @click="onMenuToggle()" />
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
