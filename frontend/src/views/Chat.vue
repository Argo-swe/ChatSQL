
<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { messageService } from '@/services/message.service'

const selectedDbms = ref("Mysql");
const dbms = ref([
    { name: 'Mysql', code: 'Mysql' },
    { name: 'PostgreSQL', code: 'PostgreSQL', },
    { name: 'MariaDB', code: 'MariaDB' },
    { name: 'Microsoft SQL Server', code: 'Microsoft' },
    { name: 'Oracle database', code: 'Oracle' },
    { name: 'SQLite', code: 'SQLite' },
]);

const selectedLanguage = ref("EN");
const languages = ref([
    { name: 'English', code: 'EN' },
    { name: 'Italian', code: 'IT' },
    { name: 'French', code: 'FR' },
    { name: 'Spanish', code: 'ES' },
    { name: 'German', code: 'DE' },
]);

const selectedDictionary = ref(null);
const dictionaries = ref([
    { name: 'Utenti', code: 'Utenti' },
    { name: 'Clienti Zucchetti', code: 'cz' },
    { name: 'Abc', code: 'abc' },
]);

const request = ref('');
const { messageSuccess, messageError, messageInfo, messageWarning } = messageService();

function runRequest() {
    console.log(request.value);
}

// Switch Hide/Show per il toggle button
const checked = ref(false);

// Variabile per controllare lo stato del container
const hide = ref(false);

const toggleSelectView = () => {
    hide.value = !hide.value;
}

// Variabile per controllare lo stato della funzione di copia del prompt
const isCopying = ref(false);

const copyToClipboard = (event) => {
    // Interrompo se c'è già una copia in corso
    if (isCopying.value) return;
    isCopying.value = true;
    // Risalgo al messaggio più vicino al bottone cliccato
    const messageContent = event.currentTarget.closest('.message').querySelector('p');
    if (!messageContent) return;
    // Estraggo il contenuto dall'elemento ed elimino eventuali spazi all'inizio e alla fine della stringa
    const text = messageContent.textContent.trim();
    navigator.clipboard.writeText(text)
        .then(() => {
            console.log('Text copied to clipboard: ', text);
            messageSuccess('Copy', 'Text copied to clipboard');
            setTimeout(() => {
                isCopying.value = false;
            }, 2000);
        })
        .catch((err) => {
            console.error('Error when copying to clipboard: ', err);
            messageError('Copy', 'Error when copying to clipboard');
        });
};

// Ritorno il nome del dizionario dati selezionato
const getDictionaryName = (code) => {
  const dict = dictionaries.value.find(dict => dict.code === code);
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
                <InputGroup class="w-fit">
                    <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name"
                        optionValue="code" placeholder="Choose dictionary..." class="max-w-12rem md:w-fit h-fit m-2 mr-0" />
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
            <div class="message sent md:w-10 mx-1 my-2">
                <div class="flex flex-row-reverse gap-3">
                    <div class="flex-shrink-0">
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                    </div>
                    <div class="w-full border-round-lg messageBox">
                        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae
                        quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo
                        rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo
                        facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
                    </div>
                </div>
            </div>

            <div class="message received md:w-10 mx-1 my-2">
                <div class="flex gap-3">
                    <div class="flex-shrink-0">
                        <Avatar icon="pi pi-database" class="" size="large" shape="circle" />
                    </div>
                    <div class="w-full border-round-lg messageBox">
                        <Button :icon="isCopying ? 'pi pi-check' : 'pi pi-copy'" class="copy-to-clipboard" severity="contrast" @click="copyToClipboard" aria-label="Copy to clipboard" />
                        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit,
                        quisquam unde dolor dicta temporibus error.</p>
                    </div>
                </div>
            </div>
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

.message {
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
