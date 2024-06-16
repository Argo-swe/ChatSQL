<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        items: [
            { label: 'Chat', icon: 'pi pi-fw pi-comments', to: '/' },
            { label: 'Dizionari dati', icon: 'pi pi-fw pi-database', to: '/dizionari' }
        ]
    },
    {
        label: 'Funzionalità tecnico',
        items: [
            { label: 'Debug', icon: 'pi pi-fw pi-eye', to: '/debug' },
            { label: 'Logout', icon: 'pi pi-fw pi-sign-out', to: '/login' }
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
