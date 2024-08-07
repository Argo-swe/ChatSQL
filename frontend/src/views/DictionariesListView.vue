<script setup lang="ts">
// External libraries
import { useConfirm } from 'primevue/useconfirm';
import { useDialog } from 'primevue/usedialog';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useMessages } from '@/composables/crud-status-messages';
import { getApiClient } from '@/services/api-client.service';
import { messageService } from '@/services/message.service';
import UtilsService from '@/services/utils.service';
import type { Components } from '@/types/openapi';

// Child Components
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';

const { t } = useI18n();
const dialog = useDialog();
const confirm = useConfirm();
let client = getApiClient();
const { messageSuccess, messageError } = messageService();

// Gain access to functions and maps to view status messages
const { getMessages, getStatusMex } = useMessages();
const onDeleteMessages = getMessages('delete');

let dictionaries = ref();
let loading = ref(false);

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
function retrieveDictionaries() {
  loading.value = true;
  dictionaries.value = [];
  client
    .getAllDictionaries()
    .then((response) => {
      if (response.data?.status == 'OK') {
        dictionaries.value = response.data.data;
      } else {
        console.warn(response.data);
      }
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('general.list.error')}\n${error.message}`);
    })
    .finally(() => {
      loading.value = false;
    });
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
function onClickDownloadFile(dictionary: Components.Schemas.DictionaryDto) {
  client
    .getDictionaryFile(dictionary.id, undefined, {
      responseType: 'blob'
    })
    .then((response) => {
      UtilsService.downloadFile(
        `${UtilsService.stringToSnakeCase(dictionary.name)}_schema.json`,
        response.data
      );
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('general.list.error')}\n${error.message}`);
    });
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
    accept: () => {
      client
        .deleteDictionary(dictionaryId)
        .then((response) => {
          if (response.data?.status == 'OK') {
            retrieveDictionaries();
            messageSuccess(t('dictionary.title'), t('actions.delete.success'));
          } else {
            messageError(
              t('dictionary.title'),
              getStatusMex(onDeleteMessages, response.data?.status, {
                message: response.data?.message,
                dictionaryId
              })
            );
          }
        })
        .catch((error) => {
          messageError(t('dictionary.title'), `${t('actions.delete.error')}\n${error.message}`);
        });
    }
  });
}
</script>

<template>
  <div class="flex justify-content-between flex-wrap">
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
        @click="onClickCreate()"
      />
    </div>
  </div>

  <PgDataTable
    :value="dictionaries"
    paginator
    :rows="10"
    :rows-per-page-options="[5, 10, 20, 50]"
    table-style="min-width: 50rem"
    :always-show-paginator="false"
    :loading="loading"
  >
    <template #empty> {{ t('general.list.empty') }} </template>
    <template #loading> {{ t('general.list.loading') }} </template>
    <PgColumn field="name" :header="t('text.Name')" sortable style="width: 25%"></PgColumn>
    <PgColumn
      field="description"
      :header="t('text.Description')"
      sortable
      style="width: 55%"
    ></PgColumn>
    <PgColumn style="width: 20%" body-style="text-align:right">
      <template #body="slotProps">
        <PgButton
          icon="pi pi-pencil"
          :title="t('dictionary.update')"
          class="ml-2"
          rounded
          @click="onClickUpdateMetadata(slotProps.data)"
        />
        <PgButton
          icon="pi pi-file-edit"
          :title="t('dictionary.file.update')"
          class="ml-2"
          rounded
          @click="onClickUpdateFile(slotProps.data)"
        />
        <PgButton
          icon="pi pi-download"
          :title="t('dictionary.file.download')"
          severity="help"
          class="ml-2"
          rounded
          @click="onClickDownloadFile(slotProps.data)"
        />
        <PgButton
          icon="pi pi-trash"
          :title="t('dictionary.delete')"
          severity="danger"
          class="ml-2"
          rounded
          @click="onClickDelete(slotProps.data.id)"
        />
      </template>
    </PgColumn>
  </PgDataTable>
</template>
