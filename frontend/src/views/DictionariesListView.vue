<script setup lang="ts">
// External libraries
import { FilterMatchMode } from 'primevue/api';
import { useConfirm } from 'primevue/useconfirm';
import { useDialog } from 'primevue/usedialog';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useMessages } from '@/composables/status-messages';
import ApiClientManager from '@/services/api-client.service';
import MessageService from '@/services/message.service';
import UtilsService from '@/services/utils.service';
import type { Components } from '@/types/openapi';

// Child Components
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';

const { t } = useI18n();
const dialog = useDialog();
const confirm = useConfirm();
const messageService = MessageService.getInstance();

// Gain access to functions and maps to view status messages
const { getMessages, getStatusMex } = useMessages();
const onDeleteMessages = getMessages('delete');

let dictionaries = ref();
let loading = ref(false);

// Define a configuration for the table filters
const filters = ref({
  name: { value: null, matchMode: FilterMatchMode.CONTAINS },
  description: { value: null, matchMode: FilterMatchMode.CONTAINS }
});

const dialogPropsPreset = {
  style: {
    width: '50vw'
  },
  breakpoints: {
    '960px': '75vw',
    '640px': '90vw'
  },
  modal: true
};

onMounted(() => {
  retrieveDictionaries();
});

/**
 * Retrieves a list of dictionaries and updates the component state accordingly.
 * @function retrieveDictionaries
 */
async function retrieveDictionaries() {
  loading.value = true;
  dictionaries.value = [];
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.getAllDictionaries();

    if (response.data?.status == 'OK') {
      dictionaries.value = response.data.data;
    } else {
      console.warn(response.data);
    }
  } catch (error) {
    messageService.messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
  } finally {
    loading.value = false;
  }
}

/**
 * Opens a dialog for creating a dictionary.
 * @function onClickCreate
 */
function onClickCreate() {
  dialog.open(CreateUpdateDictionaryModal, {
    data: {
      withFile: true
    },
    props: {
      header: t('dictionary.create'),
      ...dialogPropsPreset
    },
    onClose: (opt) => {
      if (opt?.data) {
        retrieveDictionaries();
      }
    }
  });
}

/**
 * Opens a dialog for updating the metadata of a dictionary.
 * @function onClickUpdateMetadata
 * @param dictionary - The dictionary object containing the metadata to be updated.
 */
function onClickUpdateMetadata(dictionary: Components.Schemas.DictionaryDto) {
  dialog.open(CreateUpdateDictionaryModal, {
    data: {
      withFile: false,
      dictionaryId: dictionary.id,
      dictionaryName: dictionary.name,
      dictionaryDescription: dictionary.description
    },
    props: {
      header: t('dictionary.update'),
      ...dialogPropsPreset
    },
    onClose: (opt) => {
      if (opt?.data) {
        retrieveDictionaries();
      }
    }
  });
}

/**
 * Opens a dialog for updating the file associated with a dictionary.
 * @function onClickUpdateFile
 * @param dictionary - The dictionary object containing the file to be updated.
 */
function onClickUpdateFile(dictionary: Components.Schemas.DictionaryDto) {
  dialog.open(CreateUpdateDictionaryModal, {
    data: {
      withFile: true,
      dictionaryId: dictionary.id
    },
    props: {
      header: t('dictionary.file.update'),
      ...dialogPropsPreset
    }
  });
}

/**
 * Handles the download for a file associated with a specific dictionary.
 * @function onClickDownloadFile
 * @param dictionary - The dictionary object containing metadata needed to fetch and download the file.
 */
async function onClickDownloadFile(dictionary: Components.Schemas.DictionaryDto) {
  try {
    const client = await ApiClientManager.getApiClient();
    const response = await client.getDictionaryFile(dictionary.id, undefined, {
      responseType: 'blob'
    });

    UtilsService.downloadFile(
      `${UtilsService.stringToSnakeCase(dictionary.name)}_schema.json`,
      response.data
    );
  } catch (error) {
    messageService.messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
  }
}

/**
 * Handles the deletion of a data dictionary.
 * @function onClickDelete
 * @param dictionaryId - The ID of the dictionary to be deleted.
 */
function onClickDelete(dictionaryId: number) {
  confirm.require({
    message: t('general.confirm.proceed'),
    header: t('dictionary.delete'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('text.Yes'),
    acceptClass: 'p-button-success',
    rejectLabel: t('text.No'),
    accept: async () => {
      try {
        const client = await ApiClientManager.getApiClient();
        const response = await client.deleteDictionary(dictionaryId);

        if (response.data?.status == 'OK') {
          retrieveDictionaries();
          messageService.messageSuccess(t('dictionary.title'), t('actions.delete.success'));
        } else {
          messageService.messageError(
            t('dictionary.title'),
            getStatusMex(onDeleteMessages, response.data?.status, {
              message: response.data?.message,
              dictionaryId
            })
          );
        }
      } catch (error) {
        messageService.messageError(
          t('dictionary.title'),
          `${t('actions.delete.error')}\n${error}`
        );
      }
    }
  });
}
</script>

<template>
  <div class="flex justify-content-between flex-wrap" data-testid="dictionary-page-header">
    <div class="flex m-2">
      <h1>{{ t('dictionary.title', 2) }}</h1>
    </div>
    <div class="flex m-2">
      <PgButton
        icon="pi pi-plus"
        :label="t('dictionary.create')"
        severity="success"
        class="ml-2"
        rounded
        data-testid="dictionary-create-button"
        @click="onClickCreate()"
      />
    </div>
  </div>

  <PgDataTable
    v-model:filters="filters"
    :value="dictionaries"
    filter-display="row"
    paginator
    :rows="10"
    :rows-per-page-options="[5, 10, 20, 50]"
    table-style="min-width: 50rem"
    :always-show-paginator="false"
    :loading="loading"
    data-testid="dictionaries-table"
  >
    <template #empty> {{ t('general.list.empty') }} </template>
    <template #loading> {{ t('general.list.loading') }} </template>
    <PgColumn field="name" :header="t('text.Name')" sortable style="width: 25%">
      <template #filter="{ filterModel, filterCallback }">
        <PgInputText
          v-model="filterModel.value"
          type="text"
          :placeholder="t('general.search.searchByName')"
          :aria-label="t('general.search.searchByName')"
          data-testid="search-by-name"
          @input="filterCallback()"
        />
      </template>
    </PgColumn>
    <PgColumn field="description" :header="t('text.Description')" sortable style="width: 55%">
      <template #filter="{ filterModel, filterCallback }">
        <PgInputText
          v-model="filterModel.value"
          type="text"
          :placeholder="t('general.search.searchByDescription')"
          :aria-label="t('general.search.searchByDescription')"
          data-testid="search-by-description"
          @input="filterCallback()"
        />
      </template>
    </PgColumn>
    <PgColumn style="width: 20%" body-style="text-align:right">
      <template #body="slotProps">
        <PgButton
          icon="pi pi-pencil"
          :title="t('dictionary.update')"
          class="ml-2"
          rounded
          data-testid="update-metadata-button"
          @click="onClickUpdateMetadata(slotProps.data)"
        />
        <PgButton
          icon="pi pi-file-edit"
          :title="t('dictionary.file.update')"
          class="ml-2"
          rounded
          data-testid="update-file-button"
          @click="onClickUpdateFile(slotProps.data)"
        />
        <PgButton
          icon="pi pi-download"
          :title="t('dictionary.file.download')"
          severity="help"
          class="ml-2"
          rounded
          data-testid="download-file-button"
          @click="onClickDownloadFile(slotProps.data)"
        />
        <PgButton
          icon="pi pi-trash"
          :title="t('dictionary.delete')"
          severity="danger"
          class="ml-2"
          rounded
          data-testid="dictionary-delete-button"
          @click="onClickDelete(slotProps.data.id)"
        />
      </template>
    </PgColumn>
  </PgDataTable>
</template>
