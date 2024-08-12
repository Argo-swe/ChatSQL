<script setup lang="ts">
// External libraries
import { useI18n } from 'vue-i18n';

// Internal dependencies
import type { MessageWrapper } from '@/types/wrapper';

/**
 * Props for ChatDeleteBtn component.
 */
defineProps<{
  /**
   * @prop {MessageWrapper[]} messages
   * @description An array of messages.
   */
  messages: MessageWrapper[];
  /**
   * @prop {Boolean} loading
   * @description A flag indicating whether data is loading.
   */
  loading: boolean;
}>();

/**
 * Emits for ChatDeleteBtn component.
 */
const emit = defineEmits(['clear-messages']);

const { t } = useI18n();

/**
 * Emits an event to the parent component to clear the messages.
 * @function clearMessages
 */
const clearMessages = () => {
  emit('clear-messages');
};
</script>

<template>
  <PgButton
    :label="t('chat.history.clean')"
    icon="pi pi-eraser"
    class="m-2"
    :disabled="messages.length <= 0 || loading"
    severity="danger"
    icon-pos="right"
    @click="clearMessages"
  />
</template>
