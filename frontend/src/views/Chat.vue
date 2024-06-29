<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { messageService } from '@/services/message.service'
import { getApiClient } from '@/services/api-client.service';
import ChatMessage from '@/components/ChatMessage.vue'
import AuthService from '@/services/auth.service';
import type { TabMenuChangeEvent } from 'primevue/tabmenu';
const client = getApiClient()

import { useI18n } from 'vue-i18n'
const { t } = useI18n();

let loading = ref(false);
let loadingDebug = ref(false);
let debugMessage = ref();

onMounted(() => {
    retrieveDictionaries();
    window.addEventListener('token-localstorage-changed', () => {
        isLogged.value = AuthService.isLogged();
        if (!isLogged.value) {
            active.value = 0; // show default chat tab
        }
    });
});

function retrieveDictionaries() {
    dictionaries.value = [];
    client.getAllDictionaries().then(
        response => {
            switch (response.data?.status) {
                case "OK": {
                    dictionaries.value = response.data.data;
                    let localStorageDictionaryId = localStorage.getItem('chat-dictionary-id');
                    if (localStorageDictionaryId && response.data.data.findIndex(d => d?.id) != -1) {
                        selectedDictionary.value = parseInt(localStorageDictionaryId);
                    }
                    break;
                }
                default:
                    messageError(t('dictionary.title'), `${t('general.list.error')}\n${response.data?.message}`)
            }
        },
        error => {
            messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`)
        },
    );
}

const selectedDbms = ref(localStorage.getItem('chat-dbms') || "Mysql");
const dbms = ref([
    { name: 'Mysql', code: 'Mysql' },
    { name: 'PostgreSQL', code: 'PostgreSQL', },
    { name: 'MariaDB', code: 'MariaDB' },
    { name: 'Microsoft SQL Server', code: 'Microsoft' },
    { name: 'Oracle DB', code: 'Oracle' },
    { name: 'SQLite', code: 'SQLite' },
]);

const selectedLanguage = ref(localStorage.getItem('chat-language') || "english");
const languages = ref([
    'english',
    'italian',
    'french',
    'spanish',
    'german',
]);

const selectedDictionary = ref<null|number>(null);
const dictionaries = ref();

const onLanguageChange = (value: string) => {
    localStorage.setItem('chat-language', value);
};
const onDbmsChange = (value: string) => {
    localStorage.setItem('chat-dbms', value);
};
const onDictionaryChange = (value: number) => {
    localStorage.setItem('chat-dictionary-id', value.toString());
};
const messages = ref<any>([]);

const request = ref('');
const { messageSuccess, messageError, messageInfo, messageWarning } = messageService();

function runRequest() {
    addMessage(request.value.trim(), true);
    console.log(request.value);
    loading.value = true;
    client.generatePrompt({
      dictionaryId: selectedDictionary.value!,
      query: request.value.trim(),
      dbms: selectedDbms.value,
      lang: selectedLanguage.value
    }).then(
        response => {
            switch(response.data?.status) {
                case "OK":
                    addMessage(response.data.data, false);
                break;
                case "BAD_REQUEST":
                    messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${t('actions.formatError')}`)
                break;
                default:
                    messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${response.data?.message}`)
            }
            loading.value = false;
        },
        error => {
            loading.value = false;
            messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${error}`)
        }
    )
}

function loadDebug() {
    loadingDebug.value = true;
    client.generatePromptDebug().then(
        response => {
            switch(response.data?.status) {
                case "OK":
                    debugMessage.value = response.data.data
                    break;
                case "NOT_FOUND":
                    messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${t('actions.formatError')}`)
                break;
                default:
                    messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${response.data?.message}`)
            }
            loadingDebug.value = false;
        },
        error => {
            loadingDebug.value = false;
            messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${error}`)
        }
    )
}

function addMessage(message: String, isSent: Boolean) {
    if (!messages.value) {
        messages.value = [];
    }

    messages.value.push({
        message,
        isSent
    })
}

function onTabChange(event: TabMenuChangeEvent) {
    if (event.index != 1) {
        // todo clean log
        debugMessage.value = null;
    } else {
        // load log
        loadDebug();
    }
}

let isLogged = ref(AuthService.isLogged());
const active = ref(0);
const items = ref([
    { label: () => t('chat.title'), icon: 'pi pi-comments' },
    { label: () => t('chat.debug.title'), icon: 'pi pi-receipt' }
]);


// Switch Hide/Show per il toggle button
const checked = ref(false);

// Variabile per controllare lo stato del container
const hide = ref(false);

const toggleSelectView = () => {
    hide.value = !hide.value;
}

// Ritorno il nome del dizionario dati selezionato
const getDictionaryName = (id: number | null) => {
  const dict = dictionaries.value?.find(dict => dict.id === id);
  return dict ? dict.name + ' (.json)' : t('chat.dictionary.placeholder');
};

</script>
<template>
    <TabMenu v-model:activeIndex="active" :model="items" v-if="isLogged" @tab-change="onTabChange"/>

    <div v-if="active == 0" id="chat" class="flex flex-column justify-between">
        <!-- TITLE -->
        <div id="titlebar-container" class="card p-3">
            <div id="chat-title" class="flex flex-row align-items-center">
                <h1 class="m-1 text-xl font-semibold">{{ getDictionaryName(selectedDictionary) }}</h1>
                <ToggleButton v-model="checked" :onLabel="t('text.Show')" :offLabel="t('text.Hide')" onIcon="pi pi-check" offIcon="pi pi-times" class="w-9rem m-1" aria-label="Hide or Show" @click="toggleSelectView"/>
            </div>
            <Divider :class="{hide: hide}" />
            <div :class="{hide: hide}" class="flex flex-wrap flex-row">
                <InputGroup class="w-full sm:w-fit">
                    <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name" @update:modelValue="onDictionaryChange"
                        optionValue="id" :placeholder="t('chat.dictionary.placeholder')" class="h-fit m-2 mr-0" />
                    <Button severity="info" icon="pi pi-info" class="h-fit m-2 ml-0" />
                </InputGroup>

                <Dropdown v-model="selectedDbms" :options="dbms" optionLabel="name" optionValue="code"
                    class="w-fit h-fit m-2" @update:modelValue="onDbmsChange"/>
                <Dropdown v-model="selectedLanguage" :options="languages" @update:modelValue="onLanguageChange"
                class="w-fit h-fit m-2">
                    <template #value="slotProps">
                        <div class="capitalize">
                            {{ t(`text.${slotProps.value}`) }}
                        </div>
                    </template>
                    <template #option="slotProps">
                        <div class="capitalize">
                            {{ t(`text.${slotProps.option}`) }}
                        </div>
                    </template>
                </Dropdown>
            </div>
        </div>

        <!-- CHAT MESSAGES -->
        <div id="messages">
            <ChatMessage v-for="(msg, index) in messages" :key="index" :is-sent="msg.isSent" :message="msg.message"></ChatMessage>
        </div>

        <InputGroup id="input-container" class="mt-1">
            <Textarea v-model="request" :placeholder="t('chat.prompt.placeholder')" rows="5"
                class="w-full" :aria-label="t('chat.prompt.placeholder')" />
            <Button @click="runRequest" :icon="loading ? 'pi pi-spin pi-spinner' : 'pi pi-send'" :title="t('chat.prompt.generate')" :disabled="loading || !selectedDictionary || !request" />
        </InputGroup>
    </div>

    <div v-if="active == 1" id="debug">
        <div class="card p-3">

            <h3>{{ t('chat.debug.subject') }}</h3>
            <ChatMessage v-if="!loadingDebug" :is-sent="false" :message="debugMessage"></ChatMessage>
        </div>
    </div>
</template>

<style scoped>
#chat {
    height: calc(100vh - 5rem - 4rem - 2rem);
    max-height: 100%;
    position: relative;
}

.hide {
  display: none !important;
}

#chat-title {
    justify-content: space-between;
}

#messages {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
}

#input-container {
    width: 100%;
    max-height: 10rem;
}

#input-container textarea {
    max-height: 20rem;
    overflow-y: scroll !important;
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    box-sizing: content-box;
    resize: none;
}

#input-container textarea::placeholder {
    white-space: nowrap;
}

textarea::-webkit-scrollbar {
    width: 1em;
}
</style>
