<script setup lang="ts">
// External libraries
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import type { DictionaryPreview } from '@/types/wrapper';

/**
 * Props for DictPreview component.
 */
defineProps<{
  /**
   * @prop {Boolean} detailsVisible
   * @description Flag for toggle view.
   */
  detailsVisible: boolean;
  /**
   * @prop {DictionaryPreview} dictionaryPreview
   * @description Object holding details of the data dictionary.
   */
  dictionaryPreview: DictionaryPreview;
}>();

/**
 * Emits for DictPreview component.
 */
const emit = defineEmits(['hide-details']);

const { t } = useI18n();
// Track whether the details are expanded or collapsed.
const expanded = ref(false);

/**
 * Toggles the value of the `expanded` state between true and false.
 * @function toggleExpansion
 */
const toggleExpansion = () => {
  expanded.value = !expanded.value;
};

/**
 * Emits an event to the parent component to hide dictionary details.
 * @function hideDetails
 */
const hideDetails = () => {
  emit('hide-details');
};
</script>

<template>
  <div
    v-if="detailsVisible"
    id="dictionary-details"
    :class="{ expanded: expanded }"
    class="w-full h-full"
    data-testid="dictionary-preview-container"
  >
    <div class="card h-full dict-preview">
      <PgScrollPanel class="h-full">
        <h2 data-testid="database-name">{{ dictionaryPreview.databaseName }}</h2>
        <p data-testid="database-description">{{ dictionaryPreview.databaseDescription }}</p>
        <ul data-testid="database-tables">
          <li v-for="(table, index) in dictionaryPreview.tables" :key="index" class="my-3">
            <strong>{{ table.name }}</strong
            >: {{ table.description }}
          </li>
        </ul>
      </PgScrollPanel>
      <div class="dictionary-preview-action-area">
        <PgButton
          :icon="expanded ? 'pi pi-window-minimize' : 'pi pi-expand'"
          class="m-1"
          :aria-label="expanded ? t('text.shrink_view') : t('text.expand_view')"
          data-testid="dictionary-preview-expand-button"
          @click="toggleExpansion"
        />
        <PgButton
          icon="pi pi-times"
          class="m-1"
          aria-label="t('chat.dictionary.details.hide_details')"
          data-testid="dictionary-preview-hide-button"
          @click="hideDetails"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
#dictionary-details {
  overflow-y: hidden;
}

#dictionary-details.expanded {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 999;
}

#dictionary-details .dict-preview {
  position: relative;
}

.dictionary-preview-action-area {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  z-index: 1000;
}

#dictionary-details ul {
  list-style-type: none;
  padding: 0;
}
</style>
