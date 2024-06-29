<script setup lang="ts">
import { useLayout } from '@/components/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `/layout/images/argo_trasparente.svg`;
});
</script>

<template>
    <div class="layout-footer w-full">
        <div class="titolo">
            <img :src="logoUrl" alt="Logo" height="40" class="mr-2" />
            <span class="font-medium ml-2">Gruppo ARGO</span>
        </div>
        <p class="copyright">© 2024 Gruppo ARGO<br>Tutti i diritti riservati</p>
    </div>
</template>
<style lang="scss" scoped></style>
