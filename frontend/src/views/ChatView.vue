<script setup lang="ts">
// External libraries
import type { TabMenuChangeEvent } from 'primevue/tabmenu';
import { onMounted, ref, type Ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import ChatDeleteBtn from '@/components/ChatDeleteBtn.vue';
import ChatMessage from '@/components/ChatMessage.vue';
import DictPreview from '@/components/DictPreview.vue';
import { getApiClient } from '@/services/api-client.service';
import AuthService from '@/services/auth.service';
import { messageService } from '@/services/message.service';
import UtilsService from '@/services/utils.service';
import type { DictionaryPreview, MessageWrapper } from '@/types/wrapper';

const client = getApiClient();
const { t } = useI18n();

let loading = ref(false);
let loadingDebug = ref(false);
let debugMessage = ref();

onMounted(() => {
  retrieveDictionaries()
    .then((retrieved) => {
      if (retrieved) {
        checked.value = !checked.value;
        toggleSelectView();
      }
    })
    .catch((error) => {
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
      (response) => {
        switch (response.data?.status) {
          case 'OK': {
            dictionaries.value = response.data.data;
            let localStorageDictionaryId = localStorage.getItem('chat-dictionary-id');
            if (localStorageDictionaryId && response.data.data.findIndex((d) => d?.id) != -1) {
              selectedDictionary.value = parseInt(localStorageDictionaryId);
              resolve(true);
            }
            resolve(false);
            break;
          }
          default:
            messageError(
              t('dictionary.title'),
              `${t('general.list.error')}\n${response.data?.message}`
            );
            reject(`${t('general.list.error')}\n${response.data?.message}`);
        }
      },
      (error) => {
        messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
        reject(`${t('general.list.error')}\n${error}`);
      }
    );
  });
}

// Display data dictionary preview
function getDictionaryInfo() {
  toggleDetails();
  if (!detailsVisible.value) {
    return;
  }
  client
    .getDictionaryPreview({
      id: selectedDictionary.value!
    })
    .then(
      (response) => {
        switch (response.data?.status) {
          case 'OK':
            Object.assign(dictionaryPreview.value, response.data.data);
            break;
          case 'NOT_FOUND':
            messageError(
              t('dictionary.title'),
              `${t('general.list.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: selectedDictionary.value! })}`
            );
            break;
          default:
            messageError(
              t('dictionary.title'),
              `${t('general.list.error')}\n${response.data?.message}`
            );
        }
      },
      (error) => {
        messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
      }
    );
}

const selectedDbms = ref(localStorage.getItem('chat-dbms') || 'Mysql');
const dbms = ref([
  { name: 'Mysql', code: 'Mysql' },
  { name: 'PostgreSQL', code: 'PostgreSQL' },
  { name: 'MariaDB', code: 'MariaDB' },
  { name: 'Microsoft SQL Server', code: 'Microsoft' },
  { name: 'Oracle DB', code: 'Oracle' },
  { name: 'SQLite', code: 'SQLite' }
]);

const selectedLanguage = ref(localStorage.getItem('chat-language') || 'english');
const languages = ref(['english', 'italian', 'french', 'spanish', 'german']);

const selectedDictionary = ref<null | number>(null);
const dictionaries = ref();
const dictionaryPreview: Ref<DictionaryPreview> = ref<DictionaryPreview>({
  databaseName: '',
  databaseDescription: '',
  tables: []
});

const onLanguageChange = (value: string) => {
  localStorage.setItem('chat-language', value);
};
const onDbmsChange = (value: string) => {
  localStorage.setItem('chat-dbms', value);
};
const onDictionaryChange = (value: number) => {
  localStorage.setItem('chat-dictionary-id', value.toString());
};

const messages: Ref<MessageWrapper[]> = ref<MessageWrapper[]>([]);

const clearMessages = () => {
  messages.value = [];
};

const request = ref('');
const { messageError } = messageService();

function runRequest() {
  // Hide the data dictionary preview (if visible)
  if (detailsVisible.value) {
    toggleDetails();
  }
  addMessage(request.value.trim(), true);
  console.log(request.value);
  loading.value = true;
  client
    .generatePrompt({
      dictionaryId: selectedDictionary.value!,
      query: request.value.trim(),
      dbms: selectedDbms.value,
      lang: selectedLanguage.value
    })
    .then(
      (response) => {
        switch (response.data?.status) {
          case 'OK':
            addMessage(response.data.data!, false);
            break;
          case 'BAD_REQUEST':
            messageError(
              t('chat.prompt.title'),
              `${t('actions.generate.error')}\n${t('actions.formatError')}`
            );
            break;
          default:
            messageError(
              t('chat.prompt.title'),
              `${t('actions.generate.error')}\n${response.data?.message}`
            );
        }
        loading.value = false;
      },
      (error) => {
        loading.value = false;
        messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${error}`);
      }
    );
}

function loadDebug() {
  loadingDebug.value = true;
  client.generatePromptDebug().then(
    (response) => {
      switch (response.data?.status) {
        case 'OK':
          debugMessage.value = response.data.data;
          loadingDebug.value = false;
          break;
        case 'NOT_FOUND':
          console.log(response.data.message);
          break;
        default:
          messageError(
            t('chat.debug.title'),
            `${t('actions.generate.error')}\n${response.data?.message}`
          );
      }
    },
    (error) => {
      messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${error}`);
    }
  );
}

function addMessage(message: string, isSent: boolean) {
  if (!messages.value) {
    messages.value = [];
  }

  messages.value.push({
    message,
    isSent
  });
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

// Variable to handle details visibility
const detailsVisible = ref(false);

const toggleSelectView = () => {
  hide.value = !hide.value;
};

const toggleDetails = () => {
  detailsVisible.value = !detailsVisible.value;
};

// Return selected dictionary name
const getDictionaryName = (id: number | null) => {
  const dict = dictionaries.value?.find((dict: any) => dict.id === id);
  return dict ? dict.name + ' (.json)' : t('chat.dictionary.placeholder');
};

// Download del file di log
function onClickDownloadFile() {
  UtilsService.downloadFile('chatsql_log.txt', debugMessage.value);
}
</script>
<template>
  <PgTabMenu
    v-if="isLogged"
    v-model:activeIndex="active"
    :model="items"
    class="tab-chat mb-2"
    @tab-change="onTabChange"
  />

  <div v-if="active == 0" id="chat" :class="{ isLogged: isLogged }" class="flex flex-column">
    <!-- TITLE -->
    <div id="titlebar-container" class="card p-3">
      <div id="chat-title" class="flex flex-row align-items-center">
        <h1 class="m-1 text-xl font-semibold">{{ getDictionaryName(selectedDictionary) }}</h1>
        <PgToggleButton
          v-model="checked"
          :on-label="t('text.Show')"
          :off-label="t('text.Hide')"
          on-icon="pi pi-check"
          off-icon="pi pi-times"
          class="w-9rem m-1"
          :aria-label="t('text.toggle_view')"
          @click="toggleSelectView"
        />
      </div>
      <PgDivider :class="{ hide: hide }" />
      <div :class="{ hide: hide }" class="flex flex-wrap flex-row">
        <PgInputGroup class="w-full sm:w-fit">
          <PgDropdown
            v-model="selectedDictionary"
            filter
            :options="dictionaries"
            option-label="name"
            option-value="id"
            :placeholder="t('chat.dictionary.placeholder')"
            class="h-fit m-2 mr-0"
            @update:model-value="onDictionaryChange"
          />
          <PgButton
            severity="info"
            :icon="detailsVisible ? 'pi pi-times' : 'pi pi-info'"
            class="h-fit m-2 ml-0"
            :aria-label="
              detailsVisible
                ? t('chat.dictionary.details.hide_details')
                : t('chat.dictionary.details.show_details')
            "
            @click="getDictionaryInfo()"
          />
        </PgInputGroup>

        <PgDropdown
          v-model="selectedDbms"
          :options="dbms"
          option-label="name"
          option-value="code"
          class="w-fit h-fit m-2"
          :aria-label="t('chat.dbms.placeholder')"
          @update:model-value="onDbmsChange"
        />
        <PgDropdown
          v-model="selectedLanguage"
          :options="languages"
          :aria-label="t('chat.lang.placeholder')"
          class="w-fit h-fit m-2"
          @update:model-value="onLanguageChange"
        >
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
        </PgDropdown>
        <ChatDeleteBtn
          :messages="messages"
          :loading="loading"
          @clear-messages="clearMessages"
        ></ChatDeleteBtn>
      </div>
    </div>

    <DictPreview
      :details-visible="detailsVisible"
      :dictionary-preview="dictionaryPreview"
    ></DictPreview>

    <!-- CHAT MESSAGES -->
    <div v-if="!detailsVisible" id="messages">
      <ChatMessage
        v-for="(msg, index) in messages"
        :key="index"
        :is-sent="msg.isSent"
        :message="msg.message"
      ></ChatMessage>
    </div>

    <PgInputGroup id="input-container" class="mt-1">
      <PgTextarea
        v-model="request"
        :placeholder="t('chat.prompt.placeholder')"
        rows="1"
        auto-resize
        class="w-full"
        :aria-label="t('chat.prompt.placeholder')"
      />
      <PgButton
        :icon="loading ? 'pi pi-spin pi-spinner' : 'pi pi-send'"
        :title="t('chat.prompt.generate')"
        :aria-label="t('chat.prompt.generate')"
        :disabled="loading || !selectedDictionary || !request"
        @click="runRequest"
      />
    </PgInputGroup>
  </div>

  <div v-if="active == 1" id="debug" class="h-full mt-3">
    <h1 class="m-1 mb-3 text-xl font-semibold">{{ t('chat.debug.subject') }}</h1>
    <PgButton
      v-if="!loadingDebug && debugMessage"
      icon="pi pi-download"
      :label="t('chat.debug.file.download')"
      severity="help"
      class="mb-3"
      @click="onClickDownloadFile()"
    />
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

#messages {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
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
