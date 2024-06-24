<script setup>
import { ref } from "vue";
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '@/layout/composables/layout';

const { layoutState } = useLayout();
</script>

<template>
    <div class="card flex justify-center">
        <Dialog v-model:visible="layoutState.loginDialogVisible.value" modal header="Login">
            <template #header>
                <h2>Login</h2>
            </template>
            <span class="p-text-secondary block mb-5">Login to admin area.</span>
            <div class="flex align-items-center gap-3 mb-3">
                <label for="username" class="font-semibold w-6rem">Username</label>
                <InputText id="username" class="flex-auto" autocomplete="off" />
            </div>
            <div class="flex align-items-center gap-3 mb-5">
                <label for="password" class="font-semibold w-6rem">Password</label>
                <InputText id="password" class="flex-auto" autocomplete="off" />
            </div>
            <div class="flex justify-content-end gap-2">
                <Button type="button" label="Cancel" severity="secondary"
                    @click="layoutState.loginDialogVisible.value = false"></Button>
                <Button type="button" label="Login" @click="layoutState.loginDialogVisible.value = false"></Button>
            </div>
        </Dialog>
    </div>
</template>