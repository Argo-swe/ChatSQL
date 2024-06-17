<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const { isDarkTheme } = useLayout();

</script>
<template>
    <h1>Aggiungi dizionario dati</h1>
    <FileUpload ref="fileupload" mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000"
        @upload="onUpload" />
    <Button label="Upload" @click="upload" severity="secondary" />
</template>
