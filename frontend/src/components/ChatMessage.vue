<script setup lang="ts">
// External libraries
import { useDialog } from 'primevue/usedialog';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
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
const { messageSuccess, messageError } = messageService();
const isCopying = ref(false);
const { message, debug, isSent, fullWidth } = props;

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
 * Copy the provided text to the clipboard.
 * @param text - The text to copy to the clipboard.
 */
const performCopy = (text: string) => {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      messageSuccess(t('general.clipboard.name'), t('general.clipboard.success'));
      setTimeout(() => {
        isCopying.value = false;
      }, 2000);
    })
    .catch(() => {
      messageError(t('general.clipboard.name'), t('general.clipboard.error'));
    });
};

/**
 * Event handler to copy the text from the message element closest to the clicked button.
 * @param event - The event object from the click event.
 */
const copyToClipboard = (event: any) => {
  if (isCopying.value) return;
  isCopying.value = true;

  // Go back to the message closest to the button clicked
  const messageContent = event.currentTarget.closest('.message').querySelector('p');
  if (messageContent) {
    // Extract the text and remove spaces at the beginning and end of the string
    const text = messageContent.textContent.trim();
    performCopy(text);
  }
};
</script>

<template>
  <div
    class="message mx-1 my-2"
    :class="{
      sent: isSent,
      received: !isSent,
      'md:w-10': !fullWidth
    }"
  >
    <div class="flex gap-3" :class="isSent ? 'flex-row-reverse' : ''">
      <div class="flex-shrink-0">
        <PgAvatar v-if="isSent" icon="pi pi-user" size="large" shape="circle" />
        <PgAvatar v-else icon="pi pi-database" class="" size="large" shape="circle" />
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
            @click="copyToClipboard"
          />
          <PgButton
            v-if="!isSent && debug"
            icon="pi pi-receipt"
            outlined
            class="m-1"
            severity="contrast"
            :title="t('chat.actions.open_debug')"
            :aria-label="t('chat.actions.open_debug')"
            @click="openDebugMessage"
          />
        </div>
        <p>{{ message }}</p>
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
