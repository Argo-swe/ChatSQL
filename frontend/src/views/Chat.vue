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

</script>
<template>

    <div id="chat"
        style="display: flex; flex-direction: column; justify-content: space-between; height: 78vh; width: 100%;">
        <!-- TITLE -->
        <div id="chat-title" style="width: 100%;height: 2em;">
            <h3>Nome dizionario dati</h3>
        </div>

        <!-- CHAT MESSAGES -->
        <div id="messages" style="height: 100%; display: flex; flex-direction: column; overflow-y: scroll;">
            <div class="message sent" style="background-color: rgb(218, 232, 239); width: 80%; align-self: flex-end; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
            </div>
            <div class="message recieved" style="background-color: rgb(231, 231, 232); width: 80%; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit, quisquam unde dolor dicta temporibus error.</p>
            </div>
            <div class="message sent" style="background-color: rgb(218, 232, 239); width: 80%; align-self: flex-end; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
            </div>
            <div class="message recieved" style="background-color: rgb(231, 231, 232); width: 80%; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit, quisquam unde dolor dicta temporibus error.</p>
            </div>
            <div class="message sent" style="background-color: rgb(218, 232, 239); width: 80%; align-self: flex-end; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
            </div>
            <div class="message recieved" style="background-color: rgb(231, 231, 232); width: 80%; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit, quisquam unde dolor dicta temporibus error.</p>
            </div>
            <div class="message sent" style="background-color: rgb(218, 232, 239); width: 80%; align-self: flex-end; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Autem unde tenetur labore accusantium quae quia inventore quisquam eligendi aliquid doloremque qui amet sit et cum cupiditate consectetur quo rerum maiores adipisci assumenda impedit, sequi excepturi. Adipisci, in. Similique, natus illo facere, quas, ea optio saepe architecto unde aliquid vero itaque!</p>
            </div>
            <div class="message recieved" style="background-color: rgb(231, 231, 232); width: 80%; margin: 0.5em; padding: 1em;">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium voluptatem soluta quidem ea sit, quisquam unde dolor dicta temporibus error.</p>
            </div>
        </div>

        <!-- INPUT select e promot -->
        <div id="input-container" class="flex" style="align-items: flex-end; width: 100%; margin-top: 1em;">
            <Dropdown v-model="selectedDbms" :options="dbms" optionLabel="name" optionValue="code"
                style="width: fit-content; height: fit-content;" class="" />
            <Dropdown v-model="selectedLanguage" :options="languages" optionLabel="name" optionValue="code"
                style="width: fit-content;  height: fit-content;" class="" />
            <Textarea v-model="value" placeholder="Enter a natural language request" rows="2"
                style="height: fit-content; width: 80%;" />

            <Button label="Send" icon="pi pi-send" style="width: fit-content; height: fit-content;" />
        </div>

    </div>


</template>
