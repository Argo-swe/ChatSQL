<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/components/layout/composables/layout';

const { isDarkTheme } = useLayout();

</script>
<template>
    <h1>Debug</h1>
</template>
