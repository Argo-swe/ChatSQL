<script setup lang="ts">
// External libraries
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useLayout } from '@/composables/layout';
import { useMessages } from '@/composables/status-messages';
import { getApiClient } from '@/services/api-client.service';
import { messageService } from '@/services/message.service';

const { t } = useI18n();
const client = getApiClient();
const { layoutState } = useLayout();
const { messageSuccess, messageError } = messageService();
const username = ref(null);
const password = ref(null);

// Gain access to functions and maps to view status messages
const { onLoginMessages, getStatusMex } = useMessages();

function resetForm() {
  username.value = null;
  password.value = null;
}

/**
 * Handles a successful login by:
 * - Storing the access token;
 * - Hiding the login dialog;
 * - Resetting the form fields.
 * @function handleSuccessfulLogin
 * @param accessToken - The access token to store in localStorage.
 */
const handleSuccessfulLogin = (accessToken: string) => {
  localStorage.setItem('token', accessToken);
  layoutState.loginDialogVisible.value = false;
  resetForm();
  window.dispatchEvent(
    new CustomEvent('token-localstorage-changed', {
      detail: {
        storage: localStorage.getItem('token')
      }
    })
  );
};

/**
 * Submits the login form with the provided username and password.
 * @function submitForm
 */
async function submitForm() {
  client
    .login(undefined, { username: username.value ?? '', password: password.value ?? '' })
    .then((response) => {
      if (response.data.status === 'OK') {
        const accessToken = response.data.data?.access_token || '';
        messageSuccess(
          t('Login'),
          getStatusMex(onLoginMessages, response.data.status, {
            message: response.data.message,
            username: username.value
          })
        );
        handleSuccessfulLogin(accessToken);
      } else {
        messageError(
          t('Login'),
          getStatusMex(onLoginMessages, response.data.status, {
            message: response.data.message,
            username: username.value
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('Login'), `${t('text.genericError')}:\n${error.message}`);
    });
}
</script>

<template>
  <div class="card flex justify-center">
    <PgDialog v-model:visible="layoutState.loginDialogVisible.value" modal header="Login">
      <template #header>
        <h2>{{ t('login.title') }}</h2>
      </template>
      <form>
        <span class="p-text-secondary block mb-5">{{ t('login.subject') }}</span>
        <div class="flex align-items-center gap-3 mb-3">
          <label for="username" class="font-semibold w-6rem">{{ t('text.Username') }}</label>
          <PgInputText id="username" v-model="username" class="flex-auto" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
          <label for="password" class="font-semibold w-6rem">{{ t('text.Password') }}</label>
          <PgPassword v-model="password" input-id="password" :feedback="false"></PgPassword>
        </div>
        <div class="flex justify-content-end gap-2">
          <PgButton
            type="button"
            :label="t('text.Cancel')"
            severity="secondary"
            @click="layoutState.loginDialogVisible.value = false"
          ></PgButton>
          <PgButton :label="t('text.Login')" @click="submitForm"></PgButton>
        </div>
      </form>
    </PgDialog>
  </div>
</template>
