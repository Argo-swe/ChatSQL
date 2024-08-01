<script setup lang="ts">
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';
import { getApiClient } from '@/services/api-client.service';
import UtilsService from '@/services/utils.service';
import type { Components } from '@/types/openapi';
import { useConfirm } from 'primevue/useconfirm';
import { useDialog } from 'primevue/usedialog';
import { onMounted, ref } from 'vue';

import { messageService } from '@/services/message.service';
const { messageSuccess, messageError } = messageService();

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const dialog = useDialog();
const confirm = useConfirm();

let client = getApiClient();

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

function retrieveDictionaries() {
  loading.value = true;
  dictionaries.value = [];
  client.getAllDictionaries().then(
    (response) => {
      switch (response.data?.status) {
        case 'OK':
          dictionaries.value = response.data.data;
          break;
        default:
          console.warn(response.data);
      }
      loading.value = false;
    },
    (error) => {
      loading.value = false;
      messageError(t('dictionary.title'), `${t('general.list.error')}\n${error}`);
    }
  );
}

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
      if (opt?.data == true) {
        retrieveDictionaries();
      }
    }
  });
}

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
      if (opt?.data == true) {
        retrieveDictionaries();
      }
    }
  });
}

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

function onClickDownloadFile(dictionary: Components.Schemas.DictionaryDto) {
  client
    .getDictionaryFile(dictionary.id, undefined, {
      responseType: 'blob'
    })
    .then(
      (response) => {
        UtilsService.downloadFile(
          `${UtilsService.stringToSnakeCase(dictionary.name)}_schema.json`,
          response.data
        );
      },
      (error) => {
        console.warn(error);
      }
    );
}

function onClickDelete(dictionaryId: number) {
  confirm.require({
    message: t('general.confirm.proceed'),
    header: t('dictionary.delete'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('text.Yes'),
    acceptClass: 'p-button-success',
    rejectLabel: t('text.No'),
    accept: () => {
      client.deleteDictionary(dictionaryId).then(
        (response) => {
          switch (response.data?.status) {
            case 'OK':
              retrieveDictionaries();
              messageSuccess(t('dictionary.title'), t('actions.delete.success'));
              break;
            case 'NOT_FOUND':
              messageError(
                t('dictionary.title'),
                `${t('actions.delete.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`
              );
              break;
            default:
              messageError(
                t('dictionary.title'),
                `${t('actions.delete.error')}\n${response.data?.message}`
              );
          }
        },
        (error) => {
          messageError(t('dictionary.title'), `${t('actions.delete.error')}\n${error}`);
        }
      );
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
