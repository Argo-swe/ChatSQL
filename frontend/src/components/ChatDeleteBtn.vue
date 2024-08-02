<script lang="ts">
// External libraries
import { defineComponent, PropType } from 'vue';
import { useI18n } from 'vue-i18n';

interface MessageWrapper {
  message?: string;
  isSent: boolean;
}

export default defineComponent({
  name: 'ChatDeleteBtn',
  /**
   * Props for ChatDeleteBtn component.
   * @prop {Array.<MessageWrapper>} messages - An array of message objects.
   * @prop {Boolean} loading - A flag indicating whether data is loading.
   */
  props: {
    messages: {
      type: Array as PropType<MessageWrapper[]>,
      required: true
    },
    loading: {
      type: Boolean,
      required: true
    }
  },
  emits: ["clear-messages"],

  setup(props, { emit }) {
    const { t } = useI18n();

    /**
     * Emits an event to the parent component to clear the messages.
     * @function clearMessages
    */
    const clearMessages = () => {
      emit('clear-messages')
    };

    return {
      t,
      clearMessages
    };
  }
});
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

<style scoped></style>
