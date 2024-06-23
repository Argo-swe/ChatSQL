<script setup lang="ts">
import { inject, onMounted, ref, type Ref } from "vue";
import FileUpload, { type FileUploadSelectEvent } from 'primevue/fileupload';
import { getApiClient } from '@/services/api-client.service';
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'

const client = getApiClient();
const dialogRef = inject<Ref<DynamicDialogInstance>>('dialogRef')

let onCreation = ref(true);
let withFile = ref(true);

let dictionaryId = ref();
let dictionaryName = ref('');
let dictionaryDescription = ref('');

let fileSelected = ref(false);
let fileUpload = ref();

let selectedFile: string | null;


onMounted(() => {
  const props = dialogRef?.value.data;

  onCreation.value = props?.dictionaryId == null;
  withFile.value = props?.withFile;
  dictionaryId.value = props?.dictionaryId;
  dictionaryName.value = props?.dictionaryName;
  dictionaryDescription.value = props?.dictionaryDescription;
})

const closeDialog = (status: boolean) => {
    dialogRef?.value.close(status);
}

function createDictionary() {
  client.createDictionary(
    {
      name: dictionaryName.value,
      description: dictionaryDescription.value
    },
    {
      file: selectedFile!,
    },
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(
    response => {
      switch(response.data?.status) {
        case "OK":
          closeDialog(true)
          break;
        case "BAD_REQUEST":
          //add toast with message response.data.message
          break;
        default:
          console.warn(response.data);
      }
    },
    error => {
      //add toast with generic error message
      console.error(error);
    }
  )
}

function editDictionaryMetadata() {
  client.updateDictionaryMetadata(dictionaryId.value, {
    id: dictionaryId.value,
    name: dictionaryName.value,
    description: dictionaryDescription.value
  }).then(
    response => {
      switch(response.data?.status) {
        case "OK":
          closeDialog(true)
          break;
        case "BAD_REQUEST":
          //add toast with message response.data.message
          break;
        case "NOT_FOUND":
          //add toast with message response.data.message
          break;
        default:
          console.warn(response.data);
      }
    },
    error => {
      //add toast with generic error message
      console.error(error);
    }
  )
}

function editDictionaryFile() {
  client.updateDictionaryFile(
    dictionaryId.value,
    {
      file: selectedFile!,
    },
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(
    response => {
      switch(response.data?.status) {
        case "OK":
          closeDialog(true)
          break;
        case "NOT_FOUND":
          //add toast with message response.data.message
          break;
        default:
          console.warn(response.data);
      }
    },
    error => {
      //add toast with generic error message
      console.error(error);
    }
  )
}

function submitForm() {
  if (onCreation.value) {
    createDictionary();
  } else {
    if (withFile.value) {
      editDictionaryFile()
    } else {
      editDictionaryMetadata();
    }
  }
}

function isFileSelected(): boolean {
  return !withFile.value || selectedFile != null;
}

function isFormValid(): boolean {
  return isFileSelected();
}

function clearSelectedFile() {
  fileUpload.value.clear();
  selectedFile = null;
  fileSelected.value = false;
}

const onSelectedFile = async (event: FileUploadSelectEvent) => {
  selectedFile = event.files[0];
  fileSelected.value = selectedFile != null;
}

</script>

<template>
  <form @submit.prevent="submitForm">
    <div v-if="onCreation || !withFile" class="mb-4">
      <div class="flex flex-column gap-2">
        <label for="name">Name</label>
        <InputText id="name" v-model="dictionaryName" required aria-describedby="name-help" autocomplete="off" />
      </div>
      <div class="flex flex-column gap-2 mt-4">
        <label for="description">Description</label>
        <InputText id="description" v-model="dictionaryDescription" required aria-describedby="description-help" autocomplete="off" />
      </div>
    </div>

    <div v-if="onCreation || withFile" class="flex flex-wrap">
      <Button icon="pi pi-times" class="mr-2" severity="danger" v-if="fileSelected" @click="clearSelectedFile()" aria-label="Clear file" />
      <FileUpload ref="fileUpload" mode="basic" name="demo[]" accept="application/json" required chooseLabel="Upload file" @select="onSelectedFile" :disabled="fileSelected"/>
    </div>

    <div class="flex justify-content-between flex-wrap">
        <div class="flex">
        </div>
        <div class="flex">
          <Button :label="'Save'" type="submit" class="mt-4" severity="success" :disabled="!isFormValid()" />
        </div>
    </div>
  </form>
</template>
