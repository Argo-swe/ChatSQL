<script setup lang="ts">
// External libraries
import type { TabMenuChangeEvent } from 'primevue/tabmenu';
import { onMounted, ref, type Ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useMessages } from '@/composables/status-messages';
import { getApiClient } from '@/services/api-client.service';
import AuthService from '@/services/auth.service';
import { messageService } from '@/services/message.service';
import UtilsService from '@/services/utils.service';
import type { Components } from '@/types/openapi';
import type { DictionaryPreview, MessageWrapper } from '@/types/wrapper';

// Child Components
import ChatDeleteBtn from '@/components/ChatDeleteBtn.vue';
import ChatMessage from '@/components/ChatMessage.vue';
import DictPreview from '@/components/DictPreview.vue';

const { t } = useI18n();
const client = getApiClient();
const { messageError } = messageService();

// Gain access to functions and maps to view status messages
const { getMessages, onGenerateMessages, getStatusMex } = useMessages();
const onRetrieveMessages = getMessages('read');

const active = ref(0);
const items = ref([
  { label: () => t('chat.title'), icon: 'pi pi-comments' },
  { label: () => t('chat.debug.title'), icon: 'pi pi-receipt' }
]);
let isLogged = ref(AuthService.isLogged());

const messages: Ref<MessageWrapper[]> = ref<MessageWrapper[]>([]);
let debugMessage = ref();
const dictionaries = ref<Components.Schemas.DictionaryDto[] | null[]>();
const selectedDictionary = ref<null | number>(null);
const languages = ref(['english', 'italian', 'french', 'spanish', 'german']);
const selectedLanguage = ref(localStorage.getItem('chat-language') || 'english');
const dbms = ref([
  { name: 'Mysql', code: 'Mysql' },
  { name: 'PostgreSQL', code: 'PostgreSQL' },
  { name: 'MariaDB', code: 'MariaDB' },
  { name: 'Microsoft SQL Server', code: 'Microsoft' },
  { name: 'Oracle DB', code: 'Oracle' },
  { name: 'SQLite', code: 'SQLite' }
]);
const selectedDbms = ref(localStorage.getItem('chat-dbms') || 'Mysql');
// Variable to control the state of the form container
const hide = ref(false);
// Hide/Show switch for the toggle button
const checked = ref(false);

// Variable to handle details visibility
const detailsVisible = ref(false);
const dictionaryPreview: Ref<DictionaryPreview> = ref<DictionaryPreview>({
  databaseName: '',
  databaseDescription: '',
  tables: []
});

let loading = ref(false);
let loadingDebug = ref(false);
const request = ref('');

onMounted(() => {
  retrieveDictionaries();

  window.addEventListener('token-localstorage-changed', () => {
    isLogged.value = AuthService.isLogged();
    if (!isLogged.value) {
      // Shows the default chat tab
      active.value = 0;
    }
  });
});

/**
 * Handles the tab change event.
 * @param event - The event object of type TabMenuChangeEvent.
 */
function onTabChange(event: TabMenuChangeEvent) {
  if (event.index != 1) {
    debugMessage.value = null;
  } else {
    loadDebug();
  }
}

/**
 * Saves the selected language to localStorage.
 * @param value - The selected language code to be saved.
 */
const onLanguageChange = (value: string) => {
  localStorage.setItem('chat-language', value);
};

/**
 * Saves the selected DBMS to localStorage.
 * @param value - The selected DBMS code to be saved.
 */
const onDbmsChange = (value: string) => {
  localStorage.setItem('chat-dbms', value);
};

/**
 * Saves the selected dictionary to localStorage.
 * @param value - The selected dictionary ID to be saved.
 */
const onDictionaryChange = (value: number) => {
  localStorage.setItem('chat-dictionary-id', value.toString());
};

/**
 * Returns the selected dictionary name.
 * @param id - The ID of the dictionary.
 */
const getDictionaryName = (id: number | null) => {
  const dict = dictionaries.value?.find(
    (dict: Components.Schemas.DictionaryDto | null) => dict?.id === id
  );
  return dict ? dict.name + ' (.json)' : t('chat.dictionary.placeholder');
};

/**
 * Toggles the visibility of the chat options form.
 */
const toggleSelectView = () => {
  hide.value = !hide.value;
};

/**
 * Toggles the visibility of the dictionary preview card.
 */
const toggleDetails = () => {
  if (!detailsVisible.value) {
    getDictionaryInfo();
  }
  detailsVisible.value = !detailsVisible.value;
};

/**
 * Adds a new message to the messages array.
 * @param message - The content of the message.
 * @param isSent - A flag indicating whether the message has been sent or received by the user.
 */
function addMessage(message: string, isSent: boolean) {
  if (!messages.value) {
    messages.value = [];
  }

  messages.value.push({
    message,
    isSent
  });
}

/**
 * Clears all messages from the messages array.
 */
const clearMessages = () => {
  messages.value = [];
};

/**
 * Handles the response of a read operation.
 * @function handleSuccessfulRetrieve
 * @param response - The response object returned from the read operation.
 */
function handleSuccessfulRetrieve(response: any) {
  dictionaries.value = response.data?.data;
  let localStorageDictionaryId = localStorage.getItem('chat-dictionary-id');
  if (localStorageDictionaryId && response.data?.data.findIndex((d) => d?.id) != -1) {
    selectedDictionary.value = parseInt(localStorageDictionaryId);
    checked.value = !checked.value;
    toggleSelectView();
  }
}

/**
 * Retrieves a list of dictionaries and updates the component state accordingly.
 * @function retrieveDictionaries
 */
function retrieveDictionaries() {
  dictionaries.value = [];
  client
    .getAllDictionaries()
    .then((response) => {
      if (response.data?.status == 'OK') {
        handleSuccessfulRetrieve(response);
      } else {
        messageError(
          t('dictionary.title'),
          getStatusMex(onRetrieveMessages, response.data?.status, {
            message: response.data?.message
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('general.list.error')}\n${error.message}`);
    });
}

/**
 * Retrieves detailed information about the selected dictionary.
 * @function getDictionaryInfo
 */
function getDictionaryInfo() {
  client
    .getDictionaryPreview({
      id: selectedDictionary.value!
    })
    .then((response) => {
      if (response.data?.status == 'OK') {
        Object.assign(dictionaryPreview.value, response.data?.data);
        toggleDetails();
      } else {
        messageError(
          t('dictionary.title'),
          getStatusMex(onRetrieveMessages, response.data?.status, {
            message: response.data?.message,
            dictionaryId: selectedDictionary.value!
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('general.list.error')}\n${error.message}`);
    });
}

/**
 * Prepares the prompt generation request.
 * @function setUpRequest
 */
function setUpRequest() {
  // Hide the data dictionary preview (if visible)
  if (detailsVisible.value) {
    toggleDetails();
  }
  addMessage(request.value.trim(), true);
  loading.value = true;
}

/**
 * Executes the prompt generation request.
 * @function runRequest
 */
function runRequest() {
  setUpRequest();
  client
    .generatePrompt({
      dictionaryId: selectedDictionary.value!,
      query: request.value.trim(),
      dbms: selectedDbms.value,
      lang: selectedLanguage.value
    })
    .then((response) => {
      if (response.data?.status == 'OK') {
        addMessage(response.data.data!, false);
      } else {
        messageError(
          t('chat.prompt.title'),
          getStatusMex(onGenerateMessages, response.data?.status, {
            message: response.data?.message
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${error}`);
    })
    .finally(() => {
      loading.value = false;
    });
}

/**
 * Loads debug information about the prompt generation process.
 */
function loadDebug() {
  loadingDebug.value = true;
  client
    .generatePromptDebug()
    .then((response) => {
      if (response.data?.status == 'OK') {
        debugMessage.value = response.data.data;
      } else {
        messageError(
          t('chat.debug.title'),
          getStatusMex(onGenerateMessages, response.data?.status, {
            message: response.data?.message
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('chat.debug.title'), `${t('actions.generate.error')}\n${error}`);
    })
    .finally(() => {
      loadingDebug.value = false;
    });
}

/**
 * Download a log file.
 */
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
            @click="toggleDetails"
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
