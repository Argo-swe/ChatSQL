<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const { isDarkTheme } = useLayout();

</script>
<template>
    <h1>Dizionari dati</h1>
</template>
