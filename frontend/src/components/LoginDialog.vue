<script setup lang="ts">
import { ref } from 'vue';
import { useLayout } from '@/components/layout/composables/layout';
import { getApiClient } from '@/services/api-client.service';
import { useRouter } from 'vue-router'
import { messageService } from '@/services/message.service'
const { messageSuccess, messageError, messageInfo, messageWarning } = messageService();

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const { layoutState } = useLayout();
const router = useRouter();
const client = getApiClient();

const username = ref(null);
const password = ref(null);

function resetForm() {
    username.value = null;
    password.value = null;
}

async function submitForm() {

    client.login(
        undefined,
        { "username": username.value ?? "", "password": password.value ?? "" }
    ).then(
        response => {
            switch (response.data.status) {
                case "OK":
                    localStorage.setItem("token", response.data.data?.access_token || '');
                    layoutState.loginDialogVisible.value = false
                    resetForm();
                    window.dispatchEvent(new CustomEvent('token-localstorage-changed', {
                        detail: {
                            storage: localStorage.getItem('token')
                        }
                    }));
                    break;
                case "NOT_FOUND":
                    messageError(t('Login'), t('actions.notFoundById', { item: t('text.User'), name: username.value }))
                    break;
                case "BAD_CREDENTIAL":
                    messageError(t('Login'), t('login.badCredential'))
                    break;
                default:
                    messageError(t('Login'), `${t('text.genericError')}:\n${response.data.message}`);
                    break;
            }
        },
        error => {
            messageError(t('Login'), `${t('text.genericError')}:\n${error}`);
        }
    )

}
</script>

<template>
    <div class="card flex justify-center">
        <Dialog v-model:visible="layoutState.loginDialogVisible.value" modal header="Login">
            <template #header>
                <h2>{{ t('login.title') }}</h2>
            </template>
            <form>
                <span class="p-text-secondary block mb-5">{{ t('login.subject') }}</span>
                <div class="flex align-items-center gap-3 mb-3">
                    <label for="username" class="font-semibold w-6rem">{{ t('text.Username') }}</label>
                    <InputText id="username" class="flex-auto" v-model="username" />
                </div>
                <div class="flex align-items-center gap-3 mb-5">
                    <label for="password" class="font-semibold w-6rem">{{ t('text.Password') }}</label>
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
                    <Button type="button" :label="t('text.Cancel')" severity="secondary"
                        @click="layoutState.loginDialogVisible.value = false"></Button>
                    <Button @click="submitForm" :label="t('text.Login')"></Button>
                </div>
            </form>
        </Dialog>
    </div>
</template>
