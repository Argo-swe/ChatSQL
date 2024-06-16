<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `/layout/images/argo_trasparente.svg`;
});
</script>

<template>
    <div class="layout-footer">
        <img :src="logoUrl" alt="Logo" height="40" class="mr-2" />
        <span class="font-medium ml-2">Gruppo ARGO</span>
    </div>
</template>
<style lang="scss" scoped></style>
