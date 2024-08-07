<script setup lang="ts">
import { messageService } from '@/services/message.service';
import { ref } from 'vue';
const { messageSuccess, messageError } = messageService();

const props = defineProps<{
  message: string;
  isSent: boolean;
}>();

const { message, isSent } = props;

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
  navigator.clipboard
    .writeText(text)
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
          aria-label="Copy to clipboard"
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
