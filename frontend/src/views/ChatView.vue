<script setup lang="ts">
// External libraries
import { nextTick, onMounted, ref, type Ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useMessages } from '@/composables/status-messages';
import ApiClientManager from '@/services/api-client.service';
import AuthService from '@/services/auth.service';
import MessageService from '@/services/message.service';
import type { Components } from '@/types/openapi';
import {
  DbmsCode,
  DbmsName,
  Languages,
  type DbmsOption,
  type DictionaryPreview,
  type MessageWrapper
} from '@/types/wrapper';

// Child Components
import ChatDeleteBtn from '@/components/ChatDeleteBtn.vue';
import ChatMessage from '@/components/ChatMessage.vue';
import DictPreview from '@/components/DictPreview.vue';

const { t } = useI18n();
const messageService = MessageService.getInstance();
let isLogged = ref(AuthService.isLogged());

// Gain access to functions and maps to view status messages
const { getMessages, onGenerateMessages, getStatusMex } = useMessages();
const onRetrieveMessages = getMessages('read');

// Variable to control the visibility of the "Go to Bottom" button
const showGoToBottom = ref(false);
const messagesContainer: Ref<HTMLElement | null> = ref(null);
const messages: Ref<MessageWrapper[]> = ref<MessageWrapper[]>([]);
const dictionaries = ref<Components.Schemas.DictionaryDto[] | null[]>();
const selectedDictionary = ref<number | null>(null);
const languages: Ref<Languages[]> = ref([
  Languages.en,
  Languages.it,
  Languages.fr,
  Languages.es,
  Languages.ge
]);
const selectedLanguage = ref(localStorage.getItem('chat-language') || Languages.en);
const dbms: Ref<DbmsOption[]> = ref([
  { name: DbmsName.MySQL, code: DbmsCode.MySQL },
  { name: DbmsName.PostgreSQL, code: DbmsCode.PostgreSQL },
  { name: DbmsName.MariaDB, code: DbmsCode.MariaDB },
  { name: DbmsName.Microsoft, code: DbmsCode.Microsoft },
  { name: DbmsName.Oracle, code: DbmsCode.Oracle },
  { name: DbmsName.SQLite, code: DbmsCode.SQLite }
]);
const selectedDbms = ref(localStorage.getItem('chat-dbms') || DbmsCode.MySQL);
// Variable to control the state of the options form container
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
const request = ref('');

onMounted(() => {
  retrieveDictionaries();

  window.addEventListener('token-localstorage-changed', () => {
    isLogged.value = AuthService.isLogged();
  });

  loadMessagesAndScroll();
});

/**
 * Loads messages and scrolls to the bottom of the chat container.
 * @function loadMessagesAndScroll
 * @description Waits for the DOM to update with 'nextTick', then scrolls.
 */
async function loadMessagesAndScroll() {
  loadMessages();
  await nextTick();
  scrollToBottom();
}

/**
 * Handles the scroll event of the chat container.
 * @function handleScroll
 */
const handleScroll = () => {
  const container = messagesContainer.value;
  if (container) {
    const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 50;
    showGoToBottom.value = !isAtBottom;
  }
};

/**
 * Scrolls the chat container to the bottom smoothly.
 * @function scrollToBottom
 */
const scrollToBottom = () => {
  const anchor = document.getElementById('chat-hidden-anchor');
  if (messagesContainer.value && anchor) {
    anchor.scrollIntoView({ behavior: 'smooth' });
  }
};

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
 * Hides the dictionary preview card.
 */
const hideDetails = () => {
  detailsVisible.value = false;
};

/**
 * Adds a new message to the messages array.
 * @param message - The content of the message.
 * @param isSent - A flag indicating whether the message has been sent or received by the user.
 * @param debug - (Optional) The content of the debug.
 */
function addMessage(message: string | null, isSent: boolean, debug?: string) {
  messages.value.push({
    message,
    debug,
    isSent
  });

  saveMessages();
}

/**
 * Saves all chat messages in the sessionStorage.
 */
const saveMessages = () => {
  sessionStorage.setItem('chat-messages', JSON.stringify(messages.value));
};

/**
 * Loads messages from the sessionStorage and updates the chat state accordingly.
 */
const loadMessages = () => {
  const savedMessages = sessionStorage.getItem('chat-messages');
  if (savedMessages) {
    messages.value = JSON.parse(savedMessages);
  } else {
    messages.value = [];
  }
};

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
  if (
    localStorageDictionaryId &&
    response.data?.data.findIndex((d: Components.Schemas.DictionaryDto | null) => d?.id) != -1
  ) {
    selectedDictionary.value = parseInt(localStorageDictionaryId);
    checked.value = !checked.value;
    toggleSelectView();
  }
}

/**
 * Retrieves a list of dictionaries.
 * @function retrieveDictionaries
 */
async function retrieveDictionaries() {
  dictionaries.value = [];
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.getAllDictionaries();

    if (response.data?.status == 'OK') {
      handleSuccessfulRetrieve(response);
    } else {
      messageService.messageError(
        t('dictionary.title'),
        getStatusMex(onRetrieveMessages, response.data?.status, {
          message: response.data?.message
        })
      );
    }
  } catch (error) {
    messageService.messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
  }
}

/**
 * Retrieves detailed information about the selected dictionary.
 * @function getDictionaryInfo
 */
async function getDictionaryInfo() {
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.getDictionaryPreview({
      id: selectedDictionary.value!
    });

    if (response.data?.status == 'OK') {
      Object.assign(dictionaryPreview.value, response.data?.data);
      detailsVisible.value = true;
    } else {
      messageService.messageError(
        t('dictionary.title'),
        getStatusMex(onRetrieveMessages, response.data?.status, {
          message: response.data?.message,
          dictionaryId: selectedDictionary.value!
        })
      );
    }
  } catch (error) {
    messageService.messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
  }
}

/**
 * Manage the prompt generation request when the enter key is pressed.
 * @function handleEnterKeyRequest
 */
function handleEnterKeyRequest(event: any) {
  event.preventDefault();
  if (!loading.value && selectedDictionary.value && request.value) {
    runRequest();
  }
}

/**
 * Prepares the prompt generation request.
 * @function runRequest
 */
function runRequest() {
  // Hide the data dictionary preview (if visible)
  if (detailsVisible.value) {
    hideDetails();
  }
  const query = request.value.trim();
  request.value = '';
  addMessage(query, true);
  if (isLogged.value) {
    generatePromptWithDebug(query);
  } else {
    generatePrompt(query);
  }
}

/**
 * Executes the prompt generation request.
 * @function generatePrompt
 * @param query - The trimmed user request.
 */
async function generatePrompt(query: string) {
  loading.value = true;
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.generatePrompt({
      dictionaryId: selectedDictionary.value!,
      query: query,
      dbms: selectedDbms.value,
      lang: selectedLanguage.value
    });

    if (response.data?.status == 'OK') {
      addMessage(response.data.data!, false);
    } else {
      messageService.messageError(
        t('chat.prompt.title'),
        getStatusMex(onGenerateMessages, response.data?.status, {
          message: response.data?.message
        })
      );
    }
  } catch (error) {
    messageService.messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${error}`);
  } finally {
    loading.value = false;
  }
}

/**
 * Executes the prompt generation request and loads debug information about the generation process.
 * @function generatePromptWithDebug
 * @param query - The trimmed user request.
 */
async function generatePromptWithDebug(query: string) {
  loading.value = true;
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.generatePromptWithDebug({
      dictionaryId: selectedDictionary.value!,
      query: query,
      dbms: selectedDbms.value,
      lang: selectedLanguage.value
    });

    if (response.data?.status == 'OK') {
      addMessage(response.data.data?.prompt!, false, response.data.data?.debug || undefined);
    } else {
      messageService.messageError(
        t('chat.prompt.title'),
        getStatusMex(onGenerateMessages, response.data?.status, {
          message: response.data?.message
        })
      );
    }
  } catch (error) {
    messageService.messageError(t('chat.prompt.title'), `${t('actions.generate.error')}\n${error}`);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div id="chat" class="flex flex-column" data-testid="chat">
    <div id="titlebar-container" class="card p-3" data-testid="title-bar-container">
      <div id="chat-title" class="flex flex-row align-items-center">
        <h1 class="m-1 text-xl font-semibold" data-testid="selected-dictionary-name">
          {{ getDictionaryName(selectedDictionary) }}
        </h1>
        <PgToggleButton
          v-model="checked"
          :on-label="t('text.Show')"
          :off-label="t('text.Hide')"
          on-icon="pi pi-check"
          off-icon="pi pi-times"
          class="w-9rem m-1"
          :aria-label="t('text.toggle_view')"
          data-testid="title-bar-toggle-button"
          @click="toggleSelectView"
        />
      </div>
      <PgDivider :class="{ hide: hide }" />
      <div :class="{ hide: hide }" class="flex flex-wrap flex-row" data-testid="select-view">
        <PgInputGroup class="w-full sm:w-fit">
          <PgDropdown
            v-model="selectedDictionary"
            filter
            :options="dictionaries"
            option-label="name"
            option-value="id"
            :placeholder="t('chat.dictionary.placeholder')"
            :empty-message="t('primevue.emptymessage')"
            class="h-fit m-2 mr-0"
            data-testid="dictionary-dropdown"
            @update:model-value="onDictionaryChange"
          />
          <PgButton
            severity="info"
            icon="pi pi-info"
            :disabled="!selectedDictionary"
            class="h-fit m-2 ml-0"
            :title="t('chat.dictionary.details.show_details')"
            :aria-label="t('chat.dictionary.details.show_details')"
            data-testid="dictionary-preview-button"
            @click="getDictionaryInfo"
          />
        </PgInputGroup>

        <PgDropdown
          v-model="selectedDbms"
          :options="dbms"
          option-label="name"
          option-value="code"
          class="w-fit h-fit m-2"
          :aria-label="t('chat.dbms.placeholder')"
          data-testid="dbms-dropdown"
          @update:model-value="onDbmsChange"
        />
        <PgDropdown
          v-model="selectedLanguage"
          :options="languages"
          :aria-label="t('chat.lang.placeholder')"
          class="w-fit h-fit m-2"
          data-testid="language-dropdown"
          @update:model-value="onLanguageChange"
        >
          <template #value="slotProps">
            <div class="capitalize" data-testid="chat-language-option">
              {{ t(`text.${slotProps.value}`) }}
            </div>
          </template>
          <template #option="slotProps">
            <div class="capitalize" data-testid="chat-language-option">
              {{ t(`text.${slotProps.option}`) }}
            </div>
          </template>
        </PgDropdown>
        <ChatDeleteBtn
          v-show="!detailsVisible"
          :messages="messages"
          :loading="loading"
          @clear-messages="clearMessages"
        ></ChatDeleteBtn>
      </div>
    </div>

    <DictPreview
      :details-visible="detailsVisible"
      :dictionary-preview="dictionaryPreview"
      @hide-details="hideDetails"
    ></DictPreview>

    <div
      v-if="!detailsVisible"
      id="messages"
      ref="messagesContainer"
      data-testid="messages-container"
      @scroll="handleScroll"
    >
      <ChatMessage
        v-for="(msg, index) in messages"
        :key="index"
        :is-sent="msg.isSent"
        :message="msg.message"
        :debug="msg.debug"
      ></ChatMessage>
      <div id="chat-hidden-anchor" visible="false"></div>
    </div>

    <PgInputGroup id="input-container" class="mt-1" data-testid="request-container">
      <PgTextarea
        v-model="request"
        :placeholder="t('chat.prompt.placeholder')"
        rows="1"
        auto-resize
        class="w-full"
        :aria-label="t('chat.prompt.placeholder')"
        data-testid="request-input"
        @keydown.enter="handleEnterKeyRequest"
      />
      <PgButton
        :icon="loading ? 'pi pi-spin pi-spinner' : 'pi pi-send'"
        :title="t('chat.prompt.generate')"
        :aria-label="t('chat.prompt.generate')"
        :disabled="loading || !selectedDictionary || !request"
        data-testid="request-button"
        @click="runRequest"
      />
    </PgInputGroup>

    <PgButton
      v-show="showGoToBottom && !detailsVisible && messages.length > 0"
      id="go-to-bottom"
      class="w-2rem h-2rem"
      icon="pi pi-angle-double-down"
      severity="contrast"
      rounded
      outlined
      :aria-label="t('chat.actions.scroll_to_bottom')"
      data-testid="chat-scroll-to-bottom"
      @click="scrollToBottom"
    />
  </div>
</template>

<style scoped>
#chat {
  height: calc(100vh - 5rem - 4rem);
  max-height: 100%;
  position: relative;
  margin-bottom: -2rem;
}

#go-to-bottom {
  position: absolute;
  bottom: 5rem;
  right: 50%;
  transform: translateX(50%);
  z-index: 1099;
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
