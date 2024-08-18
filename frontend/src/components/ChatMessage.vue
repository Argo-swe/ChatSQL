<script setup lang="ts">
// External libraries
import { useDialog } from 'primevue/usedialog';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import AuthService from '@/services/auth.service';
import { messageService } from '@/services/message.service';
import { type MessageWrapper } from '../types/wrapper';

// Child Components
import StringDataModal from './StringDataModal.vue';

/**
 * Props for ChatMessage component.
 */
const props = defineProps<MessageWrapper>();

const { t } = useI18n();
const dialog = useDialog();
let isLogged = ref(AuthService.isLogged());
const { messageSuccess, messageError } = messageService();
const { message, debug, isSent } = props;
const isCopying = ref(false);

onMounted(() => {
  window.addEventListener('token-localstorage-changed', () => {
    isLogged.value = AuthService.isLogged();
  });
});

/**
 * Opens a modal to display the debug message.
 * @function openDebugMessage
 */
const openDebugMessage = () => {
  dialog.open(StringDataModal, {
    data: {
      stringData: props.debug
    },
    props: {
      header: t('chat.debug.title'),
      style: {
        width: '70vw'
      },
      breakpoints: {
        '960px': '75vw',
        '640px': '90vw'
      },
      modal: true
    }
  });
};

/**
 * Copy the message to the clipboard.
 */
const copyToClipboard = () => {
  isCopying.value = true;
  navigator.clipboard
    .writeText(message.trim())
    .then(() => {
      messageSuccess(t('general.clipboard.name'), t('general.clipboard.success'));
      setTimeout(() => {
        isCopying.value = false;
      }, 2000);
    })
    .catch(() => {
      messageError(t('general.clipboard.name'), t('general.clipboard.error'));
      isCopying.value = false;
    });
};
</script>

<template>
  <div
    class="message mx-1 my-2 md:w-10"
    :class="{
      sent: isSent,
      received: !isSent
    }"
    data-testid="chat-message-container"
  >
    <div class="flex gap-3" :class="isSent ? 'flex-row-reverse' : ''">
      <div class="flex-shrink-0">
        <PgAvatar
          :icon="isSent ? 'pi pi-user' : 'pi pi-database'"
          data-testid="message-avatar"
          size="large"
          shape="circle"
        />
      </div>
      <div class="w-full border-round-lg messageBox">
        <div class="message-action-area">
          <PgButton
            v-if="!isSent"
            :icon="isCopying ? 'pi pi-check' : 'pi pi-copy'"
            class="m-1"
            outlined
            severity="contrast"
            :title="t('chat.actions.copy')"
            :aria-label="t('chat.actions.copy')"
            :disabled="isCopying"
            data-testid="copy-button"
            @click="copyToClipboard"
          />
          <PgButton
            v-if="!isSent && debug && isLogged"
            icon="pi pi-question-circle"
            outlined
            class="m-1"
            severity="contrast"
            :title="t('chat.actions.open_debug')"
            :aria-label="t('chat.actions.open_debug')"
            data-testid="debug-button"
            @click="openDebugMessage"
          />
        </div>
        <p data-testid="chat-message">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  width: 95%;
  position: relative;
}

.message .p-avatar {
  margin-bottom: 0.5em;
}

.message p {
  padding: 1em;
  white-space: pre-wrap;
}

.message-action-area {
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
</style>
