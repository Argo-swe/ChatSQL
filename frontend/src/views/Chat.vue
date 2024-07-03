<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { messageService } from '@/services/message.service'
import { getApiClient } from '@/services/api-client.service';
import ChatMessage from '@/components/ChatMessage.vue'
import AuthService from '@/services/auth.service';
import type { TabMenuChangeEvent } from 'primevue/tabmenu';
import UtilsService from '@/services/utils.service';

const client = getApiClient()

import { useI18n } from 'vue-i18n'
const { t } = useI18n();

let loading = ref(false);
let loadingDebug = ref(false);
let debugMessage = ref();

onMounted(() => {
    retrieveDictionaries()
        .then(retrieved => {
            if (retrieved) {
                checked.value = !checked.value;
                toggleSelectView();
            }
        })
        .catch(error => {
            console.log(error);
        });

    window.addEventListener('token-localstorage-changed', () => {
        isLogged.value = AuthService.isLogged();
        if (!isLogged.value) {
            active.value = 0; // show default chat tab
        }
    });
});

function retrieveDictionaries() {
    return new Promise((resolve, reject) => {
        dictionaries.value = [];
        client.getAllDictionaries().then(
            response => {
                switch (response.data?.status) {
                    case "OK": {
                        dictionaries.value = response.data.data;
                        let localStorageDictionaryId = localStorage.getItem('chat-dictionary-id');
                        if (localStorageDictionaryId && response.data.data.findIndex(d => d?.id) != -1) {
                            selectedDictionary.value = parseInt(localStorageDictionaryId);
                            resolve(true);
                        }
                        resolve(false);
                        break;
                    }
                    default:
                        messageError(t('dictionary.title'), `${t('general.list.error')}\n${response.data?.message}`);
                        reject(`${t('general.list.error')}\n${response.data?.message}`);
                }
            },
            error => {
                messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
                reject(`${t('general.list.error')}\n${error}`);
            },
        );
    });
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
    if (detailsVisible.value) {
        toggleDetails();
    }
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
                    loadingDebug.value = false;
                    break;
                case "NOT_FOUND":
                    console.log(response.data.message)
                break;
                default:
                    messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${response.data?.message}`)
            }
        },
        error => {
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

// Variabile per controllare la visibilità dei dettagli
const detailsVisible = ref(false);

const toggleSelectView = () => {
    hide.value = !hide.value;
}

const toggleDetails = () => {
    detailsVisible.value = !detailsVisible.value;
}

// Ritorno il nome del dizionario dati selezionato
const getDictionaryName = (id: number | null) => {
  const dict = dictionaries.value?.find(dict => dict.id === id);
  return dict ? dict.name + ' (.json)' : t('chat.dictionary.placeholder');
};

// Download del file di log
function onClickDownloadFile() {
    UtilsService.downloadFile('chatsql_log.txt', debugMessage.value);
}

</script>
<template>
    <TabMenu v-model:activeIndex="active" :model="items" v-if="isLogged" class="tab-chat mb-2" @tab-change="onTabChange"/>

    <div v-if="active == 0" id="chat" :class="{isLogged: isLogged}" class="flex flex-column justify-between">
        <!-- TITLE -->
        <div id="titlebar-container" class="card p-3">
            <div id="chat-title" class="flex flex-row align-items-center">
                <h1 class="m-1 text-xl font-semibold">{{ getDictionaryName(selectedDictionary) }}</h1>
                <ToggleButton v-model="checked" :onLabel="t('text.Show')" :offLabel="t('text.Hide')" onIcon="pi pi-check" offIcon="pi pi-times" class="w-9rem m-1" :aria-label="t('text.toggle_view')" @click="toggleSelectView"/>
            </div>
            <Divider :class="{hide: hide}" />
            <div :class="{hide: hide}" class="flex flex-wrap flex-row">
                <InputGroup class="w-full sm:w-fit">
                    <Dropdown filter v-model="selectedDictionary" :options="dictionaries" optionLabel="name" @update:modelValue="onDictionaryChange"
                        optionValue="id" :placeholder="t('chat.dictionary.placeholder')" class="h-fit m-2 mr-0" />
                    <Button severity="info" :icon="detailsVisible ? 'pi pi-times' : 'pi pi-info'" class="h-fit m-2 ml-0" @click="toggleDetails" />
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

        <div id="content">

            <!-- DETAILS -->
            <div id="details" v-if="detailsVisible" class="flex w-full h-full">
                    <div class="desc card h-full">
                        <ScrollPanel class="h-full">
                            <h3>Database</h3>
                            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi vel doloribus quisquam soluta necessitatibus voluptatum voluptates praesentium, rerum magnam ad fugiat aspernatur consequuntur delectus pariatur cumque sint, mollitia libero officia! Ad, tenetur nulla. Sint, aspernatur quo deleniti assumenda minima, ipsam a expedita sed quod distinctio officia? Doloremque ratione illo ab. Eligendi ad, laborum accusantium eius ut sit consequuntur? Voluptates natus excepturi corrupti aliquam reiciendis porro animi rerum consequatur molestias consequuntur, qui autem ut officia deleniti voluptas reprehenderit fugiat minus hic optio neque! Officia iure fuga praesentium rerum cupiditate dicta animi quaerat explicabo itaque reprehenderit ea, eum necessitatibus velit quisquam facere. Sunt harum ratione exercitationem debitis commodi necessitatibus natus blanditiis distinctio odit! A, facere nesciunt. In dolorem amet tempore sequi animi, voluptatum ratione fugiat laudantium magnam hic? Exercitationem deleniti quam harum dignissimos quas et quae illum possimus, illo ipsum mollitia nesciunt dicta magni ex qui praesentium dolor tempora corrupti expedita ullam. Ex minima ea dolor deserunt dolores, quae repellendus? Doloribus, quibusdam aliquid magnam voluptate officiis minus. Eius possimus vitae ut nemo voluptate, facere nulla libero fuga blanditiis quis illum ipsam sunt mollitia dolor pariatur quod, odit quam officia alias quibusdam eos? Dolorum est obcaecati libero quas iusto inventore vitae earum voluptatibus!</p>
                        </ScrollPanel>

                    </div>
                    <div class="desc card h-full">
                        <ScrollPanel class="h-full">
                            <h3>Tables</h3>
                            <p>
                                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Recusandae beatae veritatis similique harum aperiam et explicabo hic voluptate aliquid? Quo sequi repudiandae tempora reprehenderit, perferendis error quas necessitatibus, incidunt, corporis blanditiis libero excepturi ut nemo? Veniam accusamus aliquid sint voluptates quos vel minus fuga, harum sapiente ratione doloremque tempore molestias blanditiis assumenda quas nihil adipisci minima corporis repellendus id laborum soluta beatae. Consequatur, doloribus, quas ipsa neque nesciunt numquam iste nemo maiores reiciendis est iure voluptatem, placeat tempora nam labore assumenda optio quae dicta excepturi commodi nihil? Maiores adipisci rerum aspernatur odit molestiae, voluptates officia? Quidem, harum. In, expedita inventore?
                            </p>
                        </ScrollPanel>               
                    </div> 
            </div>

            <!-- CHAT MESSAGES -->
            <div id="messages" v-if="!detailsVisible">
                <ChatMessage v-for="(msg, index) in messages" :key="index" :is-sent="msg.isSent" :message="msg.message"></ChatMessage>
            </div>
        </div>

        <InputGroup id="input-container" class="mt-1">
            <Textarea v-model="request" :placeholder="t('chat.prompt.placeholder')" rows="1" autoResize
                class="w-full" :aria-label="t('chat.prompt.placeholder')" />
            <Button @click="runRequest" :icon="loading ? 'pi pi-spin pi-spinner' : 'pi pi-send'" :title="t('chat.prompt.generate')" :disabled="loading || !selectedDictionary || !request" />
        </InputGroup>
    </div>

    <div v-if="active == 1" id="debug" class="h-full mt-3">
        <h1 class="m-1 mb-3 text-xl font-semibold">{{ t('chat.debug.subject') }}</h1>
        <Button v-if="!loadingDebug && debugMessage" icon="pi pi-download" :label="t('chat.debug.file.download')" severity="help" class="mb-3" @click="onClickDownloadFile()" />
        <ChatMessage v-if="!loadingDebug" :is-sent="false" :message="debugMessage"></ChatMessage>
    </div>
</template>

<style scoped>
.tab-chat * {
    background-color: transparent;
}

#chat {
    height: calc(100vh - 5rem - 4rem);
    max-height: 100%;
    position: relative;
    margin-bottom: -2rem;
}

#chat.isLogged {
    height: calc(100vh - 5rem - 4rem - 3.5rem);
}

.hide {
  display: none !important;
}

#chat-title {
    justify-content: space-between;
}

#chat #content {
    height: 100%;
    overflow-y: hidden;
}

#details .desc {
    width: 50%;
}

#details .desc:first-child {
    margin-right: 1rem;
}

#messages {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
}

@media (max-width: 991px) {
    #details {
        width: 100%;
        flex-direction: column;
        overflow-y: scroll;
    }

    #details .desc {
        width: 100%;
    }

    #details .desc:first-child {
        margin-right: unset;
    }
    
}

#input-container {
    width: 100%;
}

#input-container textarea {
    max-height: 8rem;
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
