<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { messageService } from '@/services/message.service'
import { getApiClient } from '@/services/api-client.service';
import ChatMessage from '@/components/ChatMessage.vue'
import AuthService from '@/services/auth.service';
import type { TabMenuChangeEvent } from 'primevue/tabmenu';
const client = getApiClient()

function t(str: string) {
    return str;
}

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
                case "OK":
                    dictionaries.value = response.data.data;
                    break;
                default:
                    console.warn(response.data);
            }
        },
        error => {
            //messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`)
        },
    );
}

const selectedDbms = ref("Mysql");
const dbms = ref([
    { name: 'Mysql', code: 'Mysql' },
    { name: 'PostgreSQL', code: 'PostgreSQL', },
    { name: 'MariaDB', code: 'MariaDB' },
    { name: 'Microsoft SQL Server', code: 'Microsoft' },
    { name: 'Oracle database', code: 'Oracle' },
    { name: 'SQLite', code: 'SQLite' },
]);

const selectedLanguage = ref("english");
const languages = ref([
    { name: 'English', code: 'english' },
    { name: 'Italian', code: 'italian' },
    { name: 'French', code: 'french' },
    { name: 'Spanish', code: 'spanish' },
    { name: 'German', code: 'german' },
]);

const selectedDictionary = ref(null);
const dictionaries = ref();

const messages = ref<any>([]);

const request = ref('');
const { messageSuccess, messageError, messageInfo, messageWarning } = messageService();

function runRequest() {
    addMessage(request.value.trim(), true);
    console.log(request.value);
    loading.value = true;
    client.generatePrompt({
      dictionaryId: parseInt(selectedDictionary.value!),
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
                // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${t('actions.formatError')}`)
                break;
                case "CONFLICT":
                // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName.value })}`)
                break;
                default:
                // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${response.data?.message}`)
            }
            loading.value = false;
        },
        error => {
            loading.value = false;
            // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${error}`)
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
                // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${t('actions.formatError')}`)
                break;
                default:
                // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${response.data?.message}`)
            }
            loadingDebug.value = false;
        },
        error => {
            loadingDebug.value = false;
            // messageError(t('dictionary.title'), `${t('actions.create.error')}\n${error}`)
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
    { label: 'Chat', icon: 'pi pi-comments' },
    { label: 'Debug', icon: 'pi pi-receipt' }
]);


// Switch Hide/Show per il toggle button
const checked = ref(false);

// Variabile per controllare lo stato del container
const hide = ref(false);

const toggleSelectView = () => {
    hide.value = !hide.value;
}

// Ritorno il nome del dizionario dati selezionato
const getDictionaryName = (id: number) => {
  const dict = dictionaries.value?.find(dict => dict.id === id);
  return dict ? dict.name + ' (.json)' : 'Choose a dictionary';
};

</script>
<template>
    <TabMenu v-model:activeIndex="active" :model="items" v-if="isLogged" class="tab-chat mb-2" @tab-change="onTabChange"/>

    <div v-if="active == 0" id="chat" class="flex flex-column justify-between">
        <!-- TITLE -->
        <div id="titlebar-container" class="card p-3">
            <div id="chat-title" class="flex flex-row align-items-center">
                <h1 class="m-1 text-xl font-semibold">{{ getDictionaryName(selectedDictionary) }}</h1>
                <ToggleButton v-model="checked" onLabel="Show" offLabel="Hide" onIcon="pi pi-check" offIcon="pi pi-times" class="w-9rem m-1" aria-label="Hide or Show" @click="toggleSelectView"/>
            </div>
            <Divider :class="{hide: hide}" />
            <div :class="{hide: hide}" class="flex flex-wrap flex-row">
                <InputGroup class="w-full sm:w-fit">
                    <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name"
                        optionValue="id" placeholder="Choose dictionary..." class="h-fit m-2 mr-0" />
                    <Button severity="info" icon="pi pi-info" class="h-fit m-2 ml-0" />
                </InputGroup>

                <Dropdown v-model="selectedDbms" :options="dbms" optionLabel="name" optionValue="code"
                    class="w-fit h-fit m-2" />
                <Dropdown v-model="selectedLanguage" :options="languages" optionLabel="name" optionValue="code"
                    class="w-fit h-fit m-2" />
            </div>
        </div>

        <!-- CHAT MESSAGES -->
        <div id="messages">
            <ChatMessage v-for="(msg, index) in messages" :key="index" :is-sent="msg.isSent" :message="msg.message"></ChatMessage>
        </div>

        <InputGroup id="input-container" class="mt-1">
            <Textarea v-model="request" autoResize placeholder="Enter a natural language request" rows="1"
                class="w-full" aria-label="Enter a natural language request" />
            <Button @click="runRequest" :icon="loading ? 'pi pi-spin pi-spinner' : 'pi pi-send'" aria-label="Send a request" :disabled="loading || !selectedDictionary || !request" />
        </InputGroup>
    </div>

    <div v-if="active == 1" id="debug" class="h-full mt-3">
        <h1 class="m-1 mb-3 text-xl font-semibold">Debug riferito all'ultima richiesta dell'operatore</h1>
        <ChatMessage v-if="!loadingDebug" :is-sent="false" :message="debugMessage"></ChatMessage>
    </div>
</template>

<style scoped>
.tab-chat * {
    background-color: transparent;
}

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
    max-height: 5rem;
}

#input-container textarea {
    max-height: 20rem;
    overflow-y: scroll !important;
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    box-sizing: content-box;
}

#input-container textarea::placeholder {
    white-space: nowrap;
}

textarea::-webkit-scrollbar {
    width: 1em;
}
</style>
