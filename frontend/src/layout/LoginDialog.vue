<script setup>
import { ref } from "vue";
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '@/layout/composables/layout';

const { layoutState } = useLayout();
</script>

<template>
    <div class="card flex justify-center">
        <Dialog v-model:visible="layoutState.loginDialogVisible.value" modal header="Edit Profile">
            <template #header>
                <h2>Login</h2>
            </template>
            <span class="text-surface-500 dark:text-surface-400 block mb-8">Login into the admin area.</span>
            <div class="flex items-center gap-4 mb-4">
                <label for="username" class="font-semibold w-24">Username</label>
                <InputText id="username" class="flex-auto" autocomplete="off" />
            </div>
            <div class="flex items-center gap-4 mb-2">
                <label for="email" class="font-semibold w-24">Email</label>
                <InputText id="email" class="flex-auto" autocomplete="off" />
            </div>
            <template #footer>
                <Button label="Cancel" text severity="secondary" @click="layoutState.loginDialogVisible.value = false" autofocus />
                <Button label="Save" outlined severity="primary" @click="layoutState.loginDialogVisible.value = false" autofocus />
            </template>
        </Dialog>
    </div>

</template>