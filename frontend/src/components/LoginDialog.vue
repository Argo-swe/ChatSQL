<script setup lang="ts">
// External libraries
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useLayout } from '@/composables/layout';
import { getApiClient } from '@/services/api-client.service';
import { messageService } from '@/services/message.service';
import type { Components } from '@/types/openapi';
import type { LoginErrorMessages } from '@/types/wrapper';

const { t } = useI18n();
const client = getApiClient();
const { layoutState } = useLayout();
const { messageError } = messageService();
const username = ref(null);
const password = ref(null);
const errorMessages: LoginErrorMessages = {
  NOT_FOUND: () => t('actions.notFoundById', { item: t('text.User'), name: username.value }),
  BAD_CREDENTIAL: () => t('login.badCredential')
};

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
 * @param accessToken - The access token to store in local storage.
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
 * Handles errors based on the response status.
 * @function handleError
 * @param status - The response status code indicating the type of error.
 * @param message - (Optional) Additional message to include in the error.
 */
const handleError = (status: Components.Schemas.ResponseStatusEnum, message?: string | null) => {
  const getErrorMessage = errorMessages[status];
  let errorMessage;
  if (getErrorMessage) {
    errorMessage = getErrorMessage();
  } else {
    errorMessage = `${t('text.genericError')}:\n${message}`;
  }
  messageError(t('Login'), errorMessage);
};

/**
 * Submits the login form with the provided username and password.
 * @function submitForm
 */
async function submitForm() {
  client.login(undefined, { username: username.value ?? '', password: password.value ?? '' }).then(
    (response) => {
      if (response.data.status === 'OK') {
        const accessToken = response.data.data?.access_token || '';
        handleSuccessfulLogin(accessToken);
      } else {
        handleError(response.data.status, response.data.message);
      }
    },
    (error) => {
      messageError(t('Login'), `${t('text.genericError')}:\n${error}`);
    }
  );
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
