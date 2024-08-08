<script setup lang="ts">
import { messageService } from '@/services/message.service';
import { useDialog } from 'primevue/usedialog';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import StringDataModal from './StringDataModal.vue';

const { t } = useI18n();
const { messageSuccess, messageError } = messageService();
const dialog = useDialog();

const props = defineProps<{
  message: string;
  isSent: boolean;
  debug?: string;
  fullWidth?: boolean;
}>();

const { message, debug, isSent, fullWidth } = props;

const isCopying = ref(false);

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
            @click="copyToClipboard"
          />
          <PgButton
            v-if="!isSent && debug"
            icon="pi pi-receipt"
            outlined
            class="m-1"
            severity="contrast"
            :title="t('chat.actions.open_debug')"
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
