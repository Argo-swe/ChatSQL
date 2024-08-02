<script lang="ts">
// External libraries
import { defineComponent, ref } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
    name: 'DictPreview',
    /**
     * Props for DictPreview component.
     * @prop {Boolean} detailsVisible - Flag for toggle view.
     * @prop {Object} dictionaryPreview - Object holding details of the data dictionary.
     */
    props: {
        detailsVisible: {
            type: Boolean,
            required: true
        },
        dictionaryPreview: {
            type: Object,
            required: true
        }
    },
    setup(props) {
        /**
         * @var {boolean} expanded - Track whether the details are expanded or collapsed.
         */
        const { t } = useI18n();
        const expanded = ref(false);

        /**
         * @function
         * @description Toggles the value of the `expanded` state between true and false.
         */
        const toggleExpansion = () => {
            expanded.value = !expanded.value;
        };

        return {
            t,
            expanded,
            toggleExpansion
        };
    }
});
</script>

<template>
  <div
      v-if="detailsVisible"
      id="dictionary-details"
      :class="{ expanded: expanded }"
      class="w-full h-full"
    >
      <div class="card h-full dict-preview">
        <PgScrollPanel class="h-full">
          <h2>{{ dictionaryPreview.database_name }}</h2>
          <p>{{ dictionaryPreview.database_description }}</p>
          <ul>
            <li v-for="(table, index) in dictionaryPreview.tables" :key="index" class="my-3">
              <strong>{{ table.name }}</strong
              >: {{ table.description }}
            </li>
          </ul>
        </PgScrollPanel>
        <PgButton
          :icon="expanded ? 'pi pi-window-minimize' : 'pi pi-expand'"
          class="expand-btn"
          :aria-label="expanded ? t('text.shrink_view') : t('text.expand_view')"
          @click="toggleExpansion"
        />
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

#dictionary-details .expand-btn {
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