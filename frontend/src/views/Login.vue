<script setup lang="ts">
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import { messageService } from '../services/toast-message'

import Password from 'primevue/password';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import { getApiClient } from '../services/api-client';
import { useRouter } from 'vue-router'

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
  <div class="login-view">
    <form @submit.prevent="submitForm">
      <div class="card flex justify-content-center">
        <FloatLabel>
          <InputText id="username" v-model="username" />
          <label for="username">Username</label>
        </FloatLabel>
      </div>

      <div class="card flex justify-content-center">
        <FloatLabel>
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
          <label for="password">Password</label>
        </FloatLabel>
      </div>

      <div class="card flex justify-center">
        <Button label="Submit" type="submit" />
      </div>
    </form>
  </div>
</template>

<style scoped>
.login-view {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  background-color: #1f1f1f;
  border-radius: 8px;
}

.card {
  width: 100%;
  max-width: 400px;
  margin: 1em auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.p-float-label label {
  top: 30%;
}

.p-float-label:has(input:focus) label,
.p-float-label:has(input.p-filled) label,
.p-float-label:has(input:-webkit-autofill) label,
.p-float-label:has(textarea:focus) label,
.p-float-label:has(textarea.p-filled) label,
.p-float-label:has(.p-inputwrapper-focus) label,
.p-float-label:has(.p-inputwrapper-filled) label {
  top: -1.10rem;
}

.p-button[data-v-87276d9b] {
    left: 30%
}
</style>
