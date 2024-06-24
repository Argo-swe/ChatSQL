<script setup lang="ts">
import { ref, computed } from 'vue';
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '@/layout/composables/layout';
import AppConfig from '@/layout/AppConfig.vue';
import { messageService } from '@/services/toast-message'

import Password from 'primevue/password';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import { getApiClient } from '../services/api-client';
import { useRouter } from 'vue-router'

const { layoutState } = useLayout();
const router = useRouter();

const username = ref(null);
const password = ref(null);
const { messageSuccess, messageError, messageInfo, messageWarning } = messageService();


async function submitForm() {
    console.log('Username:', username.value);
    console.log('Password:', password.value);

    // Message examples
    // messageSuccess('Login', `user: ${username.value} - psw: ${password.value}`);
    // messageInfo('Login', `user: ${username.value} - psw: ${password.value}`);
    // messageWarning('Login', `user: ${username.value} - psw: ${password.value}`);
    // messageError('Login', `user: ${username.value} - psw: ${password.value}`);

    // Add your login logic here
    const client = await getApiClient();

    const resPrompt = await client.login(
        undefined,
        { "username": username.value ?? "", "password": password.value ?? "" }
    );
    switch (resPrompt.data.status) {
        case "OK":
            localStorage.setItem("token", resPrompt.data.data?.access_token || '');
            router.push('/')
            break;
        case "NOT_FOUND":
            messageWarning('Login', `Utente '${username.value}' non trovato`);
            break;
        default:
            messageError('Login', `ERROR: ${resPrompt.data.message}`);
            break;
    }
}
</script>

<template>
    <div class="card flex justify-center">
        <Dialog v-model:visible="layoutState.loginDialogVisible.value" modal header="Login">
            <template #header>
                <h2>Login</h2>
            </template>
            <form @submit.prevent="submitForm">
                <span class="p-text-secondary block mb-5">Login to admin area.</span>
                <div class="flex align-items-center gap-3 mb-3">
                    <label for="username" class="font-semibold w-6rem">Username</label>
                    <InputText id="username" class="flex-auto" v-model="username" />
                </div>
                <div class="flex align-items-center gap-3 mb-5">
                    <label for="password" class="font-semibold w-6rem">Password</label>
                    <Password v-model="password" inputId="password">
                        <template #header>
                            <h6>Pick a password</h6>
                        </template>
                        <template #footer>
                            <Divider />
                            <p class="mt-2">Suggestions</p>
                            <ul class="pl-2 ml-2 mt-0" style="line-height: 1.5">
                                <li>At least one lowercase</li>
                                <li>At least one uppercase</li>
                                <li>At least one numeric</li>
                                <li>Minimum 8 characters</li>
                            </ul>
                        </template>
                    </Password>
                </div>
                <div class="flex justify-content-end gap-2">
                    <Button type="sumbit" label="Cancel" severity="secondary"
                        @click="layoutState.loginDialogVisible.value = false"></Button>
                    <Button type="button" label="Login" @click="layoutState.loginDialogVisible.value = false"></Button>
                </div>
            </form>
        </Dialog>
    </div>
</template>