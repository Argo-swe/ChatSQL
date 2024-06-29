<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { messageService } from '@/services/message.service'
import { getApiClient } from '@/services/api-client.service';
import ChatMessage from '@/components/ChatMessage.vue'
const client = getApiClient()

function t(str: string) {
    return str;
}

onMounted(() => {
    retrieveDictionaries();
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
        },
        error => {
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


// Switch Hide/Show per il toggle button
const checked = ref(false);

// Variabile per controllare lo stato del container
const hide = ref(false);

const toggleSelectView = () => {
    hide.value = !hide.value;
}

// Ritorno il nome del dizionario dati selezionato
const getDictionaryName = (id) => {
  const dict = dictionaries.value?.find(dict => dict.id === id);
  return dict ? dict.name + ' (.json)' : 'Choose a dictionary';
};

</script>
<template>

    <div id="chat" class="flex flex-column justify-between">
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
            <ChatMessage v-for="msg in messages" :is-sent="msg.isSent" :message="msg.message"></ChatMessage>
            <!-- <ChatMessage :is-sent="true" message="Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quorerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illofacere, quas, ea optio saepe architecto unde aliquid vero itaque!"></ChatMessage>

            <ChatMessage :is-sent="false" message="Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit,quisquam unde dolor dicta temporibus error."></ChatMessage> -->
        </div>

        <InputGroup id="input-container" class="mt-1">
            <Textarea v-model="request" autoResize placeholder="Enter a natural language request" rows="1"
                class="w-full" aria-label="Enter a natural language request" :disabled="!selectedDictionary" />
            <Button @click="runRequest" icon="pi pi-send" aria-label="Send a request" :disabled="!selectedDictionary" />
        </InputGroup>
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

/* .message {
    width: 95%;
    position: relative;
}

.message .p-avatar {
    margin-bottom: 0.5em;
}

.message p {
    padding: 1em;
}

.copy-to-clipboard {
    position: absolute;
    top: 0.1rem;
    right: 0.1rem;
}

.message.sent {
    align-self: flex-end;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.message.sent .messageBox {
    background-color: var(--message-sent);
}

.message.received .messageBox {
    background-color: var(--message-received);
} */

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
