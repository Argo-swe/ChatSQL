<script setup lang="ts">
import { getApiClient } from '@/services/api-client.service';
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions';
import { type FileUploadSelectEvent } from 'primevue/fileupload';
import { inject, onMounted, ref, type Ref } from 'vue';

import { messageService } from '@/services/message.service';
const { messageSuccess, messageError } = messageService();

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const client = getApiClient();
const dialogRef = inject<Ref<DynamicDialogInstance>>('dialogRef');

let onCreation = ref(true);
let withFile = ref(true);

let dictionaryId = ref();
let dictionaryName = ref('');
let dictionaryDescription = ref('');

let fileSelected = ref(false);
let fileUpload = ref();

let selectedFile: string | null;
let loading = ref(false);

onMounted(() => {
  const props = dialogRef?.value.data;

  onCreation.value = props?.dictionaryId == null;
  withFile.value = props?.withFile;
  dictionaryId.value = props?.dictionaryId;
  dictionaryName.value = props?.dictionaryName;
  dictionaryDescription.value = props?.dictionaryDescription;
});

const closeDialog = (status: boolean) => {
  dialogRef?.value.close(status);
};

function createDictionary() {
  loading.value = true;
  client
    .createDictionary(
      {
        name: dictionaryName.value,
        description: dictionaryDescription.value
      },
      {
        file: selectedFile!
      },
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    .then(
      (response) => {
        switch (response.data?.status) {
          case 'OK':
            messageSuccess(t('dictionary.title'), t('actions.create.success'));
            closeDialog(true);
            break;
          case 'BAD_REQUEST':
            messageError(
              t('dictionary.title'),
              `${t('actions.create.error')}\n${t('actions.formatError')}`
            );
            break;
          case 'CONFLICT':
            messageError(
              t('dictionary.title'),
              `${t('actions.create.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName.value })}`
            );
            break;
          default:
            messageError(
              t('dictionary.title'),
              `${t('actions.create.error')}\n${response.data?.message}`
            );
        }
        loading.value = false;
      },
      (error) => {
        messageError(t('dictionary.title'), `${t('actions.create.error')}\n${error}`);
        loading.value = false;
      }
    );
}

function updateDictionaryMetadata() {
  loading.value = true;
  client
    .updateDictionaryMetadata(dictionaryId.value, {
      id: dictionaryId.value,
      name: dictionaryName.value,
      description: dictionaryDescription.value
    })
    .then(
      (response) => {
        switch (response.data?.status) {
          case 'OK':
            messageSuccess(t('dictionary.title'), t('actions.update.success'));
            closeDialog(true);
            break;
          case 'BAD_REQUEST':
            messageError(
              t('dictionary.title'),
              `${t('actions.update.error')}\n${t('actions.formatError')}`
            );
            break;
          case 'NOT_FOUND':
            messageError(
              t('dictionary.title'),
              `${t('actions.update.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`
            );
            break;
          case 'CONFLICT':
            messageError(
              t('dictionary.title'),
              `${t('actions.update.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName.value })}`
            );
            break;
          default:
            messageError(
              t('dictionary.title'),
              `${t('actions.update.error')}\n${response.data?.message}`
            );
        }
        loading.value = false;
      },
      (error) => {
        messageError(t('dictionary.title'), `${t('actions.update.error')}\n${error}`);
        loading.value = false;
      }
    );
}

function updateDictionaryFile() {
  loading.value = true;
  client
    .updateDictionaryFile(
      dictionaryId.value,
      {
        file: selectedFile!
      },
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    .then(
      (response) => {
        switch (response.data?.status) {
          case 'OK':
            messageSuccess(t('dictionary.file.title'), t('actions.update.success'));
            closeDialog(true);
            break;
          case 'BAD_REQUEST':
            messageError(
              t('dictionary.file.title'),
              `${t('actions.update.error')}\n${t('actions.formatError')}`
            );
            break;
          case 'NOT_FOUND':
            messageError(
              t('dictionary.file.title'),
              `${t('actions.update.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`
            );
            break;
          default:
            messageError(
              t('dictionary.file.title'),
              `${t('actions.update.error')}\n${response.data?.message}`
            );
        }
        loading.value = false;
      },
      (error) => {
        messageError(t('dictionary.file.title'), `${t('actions.update.error')}\n${error}`);
        loading.value = false;
      }
    );
}

function submitForm() {
  if (onCreation.value) {
    createDictionary();
  } else {
    if (withFile.value) {
      updateDictionaryFile();
    } else {
      updateDictionaryMetadata();
    }
  }
}

function isFileSelected(): boolean {
  return !withFile.value || selectedFile != null;
}

function isFormValid(): boolean {
  if (onCreation.value || !withFile.value) {
    return (
      isFileSelected() &&
      dictionaryName.value?.length > 0 &&
      dictionaryDescription.value?.length > 0
    );
  } else {
    return isFileSelected();
  }
}

function clearSelectedFile() {
  fileUpload.value.clear();
  selectedFile = null;
  fileSelected.value = false;
}

const onSelectedFile = async (event: FileUploadSelectEvent) => {
  selectedFile = event.files[0];
  fileSelected.value = selectedFile != null;
};
</script>

<template>
  <form @submit.prevent="submitForm">
    <div v-if="onCreation || !withFile" class="mb-4">
      <div class="flex flex-column gap-2">
        <label for="name"> {{ t('text.Name') }} </label>
        <PgInputText
          id="name"
          v-model="dictionaryName"
          required
          aria-describedby="name-help"
          autocomplete="off"
          :invalid="!dictionaryName"
        />
      </div>
      <div class="flex flex-column gap-2 mt-4">
        <label for="description"> {{ t('text.Description') }} </label>
        <PgInputText
          id="description"
          v-model="dictionaryDescription"
          required
          aria-describedby="description-help"
          autocomplete="off"
          :invalid="!dictionaryDescription"
        />
      </div>
    </div>

    <div v-if="onCreation || withFile" class="flex flex-wrap">
      <PgButton
        v-if="fileSelected"
        icon="pi pi-times"
        class="mr-2"
        severity="danger"
        aria-label="Clear file"
        @click="clearSelectedFile()"
      />
      <PgFileUpload
        ref="fileUpload"
        mode="basic"
        name="demo[]"
        accept="application/json"
        required
        :choose-label="t('general.input.fileupload')"
        :disabled="fileSelected"
        @select="onSelectedFile"
      />
    </div>

    <div class="flex justify-content-between flex-wrap">
      <div class="flex"></div>
      <div class="flex">
        <PgButton
          :label="t('text.Save')"
          :icon="loading ? 'pi pi-spin pi-spinner' : ''"
          type="submit"
          class="mt-4"
          severity="success"
          :disabled="!isFormValid() || loading"
        />
      </div>
    </div>
  </form>
</template>
