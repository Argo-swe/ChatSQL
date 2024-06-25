<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const { isDarkTheme } = useLayout();

const selectedDbms = ref("PostgreSQL");
const dbms = ref([
    { name: 'PostgreSQL', code: 'PostgreSQL', },
    { name: 'Mysql', code: 'Mysql' },
    { name: 'MariaDB', code: 'MariaDB' },
    { name: 'Microsoft SQL Server', code: 'Microsoft' },
    { name: 'Oracle database', code: 'Oracle' },
    { name: 'SQLite', code: 'SQLite' },
]);

const selectedLanguage = ref("IT");
const languages = ref([
    { name: 'Italian', code: 'IT' },
    { name: 'English', code: 'EN' },
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

function runRequest() {
    console.log(request.value);
}

</script>
<template>

    <div id="chat" class="flex flex-column justify-between">
        <!-- TITLE -->
        <div id="chat-title" class="flex flex-row justify-between">
            <h3>Nome dizionario dati</h3>
            <Dropdown v-model="selectedDbms" :options="dbms" optionLabel="name" optionValue="code"
                class="w-fit h-fit" />
            <Dropdown v-model="selectedLanguage" :options="languages" optionLabel="name" optionValue="code"
                class="w-fit h-fit" />

            <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name"
                optionValue="code" />
            <Button severity="secondary" icon="pi pi-info" rounded />
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

            <div class="message recieved">
                <Avatar icon="pi pi-database" class="" size="large" shape="circle" />
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit,
                    quisquam unde dolor dicta temporibus error.</p>

            </div>
        </div>

        <!-- INPUT select e promot -->
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

#chat-title {
    width: 100%;
    height: 2em;
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
}

.message.sent {
    background-color: rgb(218, 232, 239);
    align-self: flex-end;
}

.message.recieved {
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