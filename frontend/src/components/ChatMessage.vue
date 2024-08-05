<script setup lang="ts">
// External libraries
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { messageService } from '@/services/message.service';
import type { MessageWrapper } from '@/types/wrapper';

/**
 * Props for ChatMessage component.
 */
const props = defineProps<MessageWrapper>();

const { t } = useI18n();
const { message, isSent } = props;
const { messageSuccess, messageError } = messageService();
const isCopying = ref(false);

/**
 * Copy the provided text to the clipboard.
 * @param text - The text to copy to the clipboard.
 */
const performCopy = (text: string) => {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      console.log(t('general.clipboard.success') + ': ', text);
      messageSuccess(t('general.clipboard.name'), t('general.clipboard.success'));
      setTimeout(() => {
        isCopying.value = false;
      }, 2000);
    })
    .catch((err) => {
      console.error(t('general.clipboard.error') + ': ', err);
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
  <div class="message md:w-10 mx-1 my-2" :class="isSent ? 'sent' : 'received'">
    <div class="flex gap-3" :class="isSent ? 'flex-row-reverse' : ''">
      <div class="flex-shrink-0">
        <PgAvatar v-if="isSent" icon="pi pi-user" size="large" shape="circle" />
        <PgAvatar v-else icon="pi pi-database" class="" size="large" shape="circle" />
      </div>
      <div class="w-full border-round-lg messageBox">
        <PgButton
          v-if="!isSent"
          :icon="isCopying ? 'pi pi-check' : 'pi pi-copy'"
          class="copy-to-clipboard"
          severity="contrast"
          :aria-label="t('general.clipboard.action')"
          @click="copyToClipboard"
        />
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
</style>
