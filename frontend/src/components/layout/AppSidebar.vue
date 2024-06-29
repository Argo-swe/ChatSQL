<script setup>
import AppMenu from './AppMenu.vue';
import AppFooter from './AppFooter.vue';
</script>

<template>
    <div class="flex flex-column justify-content-between flex-wrap">
        <div class="flex m-2">
            <app-menu></app-menu>
        </div>
        <div class="flex m-2">
            <app-footer></app-footer>
        </div>
    </div>
</template>

<style lang="scss" scoped></style>
