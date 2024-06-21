<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const { isDarkTheme } = useLayout();

</script>
<template>
    <FloatLabel>
    <InputText id="username" v-model="value" />
    <label for="username">Scrivi prompt</label>
</FloatLabel>
</template>
