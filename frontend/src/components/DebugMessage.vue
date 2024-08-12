<script setup lang="ts">
// External libraries
import { useI18n } from 'vue-i18n';

// Internal dependencies
import UtilsService from '@/services/utils.service';

/**
 * Props for DebugMessage component.
 */
const props = defineProps<{
  /**
   * @prop {String} message
   * @description A debug message.
   */
  message: string;
}>();

const { t } = useI18n();
const { message } = props;

/**
 * Download a log file.
 */
function onClickDownloadFile() {
  UtilsService.downloadFile('chatsql_log.txt', message);
}
</script>

<template>
  <div class="message mx-1">
    <div class="w-full">
      <div class="message-action-area">
        <PgButton
          icon="pi pi-download"
          class="mx-1"
          raised
          severity="danger"
          :title="t('chat.debug.file.download')"
          :aria-label="t('chat.debug.file.download')"
          @click="onClickDownloadFile"
        />
      </div>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<style scoped>
.message {
  position: relative;
}
.message p {
  padding: 0.3em 0.5em;
  white-space: pre-wrap;
}
.message-action-area {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 0.1rem;
  right: 0.1rem;
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
}
</style>
