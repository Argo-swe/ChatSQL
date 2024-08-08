<script setup lang="ts">
// External libraries
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions';
import { type FileUploadSelectEvent } from 'primevue/fileupload';
import { inject, onMounted, ref, type Ref } from 'vue';
import { useI18n } from 'vue-i18n';

// Internal dependencies
import { useMessages } from '@/composables/status-messages';
import { getApiClient } from '@/services/api-client.service';
import { messageService } from '@/services/message.service';

const { t } = useI18n();
const client = getApiClient();
const { messageSuccess, messageError } = messageService();
const dialogRef = inject<Ref<DynamicDialogInstance>>('dialogRef');

// Gain access to functions and maps to view status messages
const { getMessages, getStatusMex } = useMessages();
const onCreateMessages = getMessages('create');
const onUpdateMessages = getMessages('update');

let onCreation = ref(true);
let withFile = ref(true);

let dictionaryId = ref();
let dictionaryName = ref();
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

/**
 * Closes the dialog with a specified status.
 * @function closeDialog
 */
const closeDialog = (status: boolean) => {
  dialogRef?.value.close(status);
};

/**
 * Clears the selected file and resets related state.
 * @function clearSelectedFile
 */
function clearSelectedFile() {
  fileUpload.value.clear();
  selectedFile = null;
  fileSelected.value = false;
}

/**
 * Handles the file selection event.
 * @function onSelectedFile
 * @param event - The event triggered when a file is selected.
 */
const onSelectedFile = async (event: FileUploadSelectEvent) => {
  selectedFile = event.files[0];
  fileSelected.value = selectedFile != null;
};

/**
 * Checks if a file is selected.
 */
function isFileSelected(): boolean {
  return !withFile.value || selectedFile != null;
}

/**
 * Validates the form based on the current state.
 */
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

/**
 * Sends a request to create a new dictionary.
 * @function createDictionary
 * @description This function handles the process of uploading a new dictionary,
 * including its metadata and optional file.
 */
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
    .then((response) => {
      if (response.data?.status == 'OK') {
        messageSuccess(t('dictionary.title'), t('actions.create.success'));
        closeDialog(true);
      } else {
        messageError(
          t('dictionary.title'),
          getStatusMex(onCreateMessages, response.data?.status, {
            message: response.data?.message,
            dictionaryName: dictionaryName.value
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('actions.create.error')}\n${error.message}`);
    })
    .finally(() => {
      loading.value = false;
    });
}

/**
 * Sends a request to update the metadata of an existing dictionary.
 * @function updateDictionaryMetadata
 * @description This function updates the dictionary's name and description without changing its file.
 */
function updateDictionaryMetadata() {
  loading.value = true;
  client
    .updateDictionaryMetadata(dictionaryId.value, {
      id: dictionaryId.value,
      name: dictionaryName.value,
      description: dictionaryDescription.value
    })
    .then((response) => {
      if (response.data?.status == 'OK') {
        messageSuccess(t('dictionary.title'), t('actions.update.success'));
        closeDialog(true);
      } else {
        messageError(
          t('dictionary.title'),
          getStatusMex(onUpdateMessages, response.data?.status, {
            message: response.data?.message,
            dictionaryId: dictionaryId.value,
            dictionaryName: dictionaryName.value
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('dictionary.title'), `${t('actions.update.error')}\n${error.message}`);
    })
    .finally(() => {
      loading.value = false;
    });
}

/**
 * Sends a request to update the file associated with an existing dictionary.
 * @function updateDictionaryFile
 * @description This function updates only the file, without changing the metadata.
 */
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
    .then((response) => {
      if (response.data?.status == 'OK') {
        messageSuccess(t('dictionary.file.title'), t('actions.update.success'));
        closeDialog(true);
      } else {
        messageError(
          t('dictionary.file.title'),
          getStatusMex(onUpdateMessages, response.data?.status, {
            message: response.data?.message,
            dictionaryId: dictionaryId.value,
            dictionaryName: dictionaryName.value
          })
        );
      }
    })
    .catch((error) => {
      messageError(t('dictionary.file.title'), `${t('actions.update.error')}\n${error.message}`);
    })
    .finally(() => {
      loading.value = false;
    });
}

/**
 * Determines which action to perform based on the form's state.
 * @function submitForm
 */
function submitForm() {
  if (onCreation.value) {
    createDictionary();
  } else if (withFile.value) {
    updateDictionaryFile();
  } else {
    updateDictionaryMetadata();
  }
}
</script>

<template>
  <form @submit.prevent="submitForm">
    <div v-if="onCreation || !withFile" class="mb-4">
      <div class="flex flex-column gap-2">
        <label id="l-name" for="name"> {{ t('text.Name') }} </label>
        <PgInputText
          id="name"
          v-model="dictionaryName"
          required
          aria-labelledby="l-name"
          autocomplete="off"
          :invalid="!dictionaryName"
        />
      </div>
      <div class="flex flex-column gap-2 mt-4">
        <label id="l-description" for="description"> {{ t('text.Description') }} </label>
        <PgInputText
          id="description"
          v-model="dictionaryDescription"
          required
          aria-labelledby="l-description"
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
        :aria-label="t('dictionary.file.clear')"
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
