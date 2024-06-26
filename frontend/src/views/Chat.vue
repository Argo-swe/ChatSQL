<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { messageService } from '../services/toast-message'

const { isDarkTheme } = useLayout();

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

</script>
<template>

    <div id="chat" class="flex flex-column justify-between">
        <!-- TITLE -->
        <div class="flex flex-row align-items-center justify-content-start mb-2">
            <h3 class="m-1">Choose a dictionary</h3>
            <ToggleButton v-model="checked" onLabel="Show" offLabel="Hide" onIcon="pi pi-check" offIcon="pi pi-times" class="w-9rem m-1" aria-label="Hide or Show" @click="toggleSelectView"/>
        </div>
        <div id="chat-title" :class="{hide: hide}" class="flex flex-wrap flex-row justify-between">
            <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name"
                    optionValue="code" placeholder="Choose dictionary..." class="w-fit max-w-8rem md:max-w-max h-fit m-2" />
            <Button severity="secondary" icon="pi pi-info" rounded class="m-2" />

            <Dropdown v-model="selectedDbms" :options="dbms" optionLabel="name" optionValue="code"
                class="w-fit h-fit m-2" />
            <Dropdown v-model="selectedLanguage" :options="languages" optionLabel="name" optionValue="code"
                class="w-fit h-fit m-2" />
        </div>

        <!-- CHAT MESSAGES -->
        <div id="messages">

            <div class="message sent">
                <Avatar icon="pi pi-user" class="" size="large" shape="circle" />
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae
                    quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo
                    rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo
                    facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
            </div>

            <div class="message received border-round-lg">
                <Avatar icon="pi pi-database" class="" size="large" shape="circle" />
                <Button :label="isCopying ? '' : 'Copy'" :icon="isCopying ? 'pi pi-check' : 'pi pi-copy'" class="copy-to-clipboard" severity="contrast" @click="copyToClipboard"/>
                <p class="mt-2">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit,
                    quisquam unde dolor dicta temporibus error.
                </p>
            </div>
        </div>

        <!-- INPUT select e prompt -->
        <div id="input-container" class="absolute bottom-0 left-0 right-0 flex items-end">
            <Textarea v-model="request" autoResize placeholder="Enter a natural language request" rows="1"
                class="w-full" />
            <Button @click="runRequest" aria-label="Send" icon="pi pi-send" rounded />
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
    width: 100%;
    /* Con la gestione dello switch On/Off limitare l'altezza diventa superfluo */
    /* height: 2em; */
    background-color: var(--primary-100);
}

#messages {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
}

.message {
    width: 80%;
    padding: 1em;
    margin: 0.5em;
    /* position relative aggiunta per avere un riferimento da cui partire per spostare il copy button */
    position: relative;
}

.copy-to-clipboard {
    position: absolute;
    top: 1em;
    right: 1em;
}

.message.sent {
    background-color: rgb(218, 232, 239);
    align-self: flex-end;
}

.message.received {
    background-color: rgb(231, 231, 232);
}

#input-container {
    width: 100%;
    margin-top: 1em;
    align-items: flex-end;
    max-height: 5rem;
}

#input-container textarea {
    max-height: 20rem;
}

textarea::-webkit-scrollbar {
    width: 1em;
}
</style>