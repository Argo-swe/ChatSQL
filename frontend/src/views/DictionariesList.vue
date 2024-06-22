<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getApiClient } from '@/services/api-client';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import { useConfirm } from "primevue/useconfirm";
import { useDialog } from 'primevue/usedialog';
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';
import type { Components } from '@/types/openapi';

const dialog = useDialog();
const confirm = useConfirm();

let client = getApiClient()

let dictionaries = ref();
let loading = ref(false);

const dialogPropsPreset = {
    style: {
        width: '50vw',
    },
    breakpoints:{
        '960px': '75vw',
        '640px': '90vw'
    },
    modal: true
}

onMounted(() => {
    retrieveDictionaries();
});

function retrieveDictionaries() {
    loading.value = true;
    dictionaries.value = [];
    client.getAllDictionaries().then(
        response => {
            switch (response.data?.status) {
                case "OK":
                    dictionaries.value = response.data.data;
                    break;
                default:
                    console.warn(response.data);
            }
            loading.value = false;
        },
        error => {
            loading.value = false;
            // TODO: show error
            console.warn(error);
        },
    );
}

function onClickCreate() {
    dialog.open(CreateUpdateDictionaryModal, {
        data: {
            withFile: true,
        },
        props: {
            header: 'Create new dictionary',
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
            header: 'Update dictionary metadata',
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
            header: 'Update dictionary file',
            ...dialogPropsPreset
        }
    });
}

function onClickDelete(dictionaryId: number) {
    confirm.require({
        message: 'Are you sure you want to proceed?',
        header: 'Delete dictionary',
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
            client.deleteDictionary(dictionaryId).then(
                response => {
                    // TODO: eliminato con successo
                    retrieveDictionaries();
                    switch(response.data?.status) {
                        case "OK":
                            retrieveDictionaries();
                            break;
                        case "NOT_FOUND":
                            //add toast with message response.data.message
                            break;
                        default:
                            console.warn(response.data);
                    }
                },
                error => {
                    // TODO: eliminato con errore
                    console.warn(error);
                }
            )
        }
    });
}
</script>

<template>
    <div class="flex justify-content-between flex-wrap">
        <div class="flex m-2">
            <h1>Dizionari dati</h1>
        </div>
        <div class="flex m-2">
            <Button icon="pi pi-plus" label="Create dictionary" severity="success" class="ml-2" rounded @click="onClickCreate()" />
        </div>
    </div>

    <DataTable :value="dictionaries" paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem" :alwaysShowPaginator="false" :loading="loading">
        <template #empty> Nessun dizionario trovato </template>
        <template #loading> Caricamento dati dizionati. Attendere... </template>
        <Column field="name" header="Name" sortable style="width: 25%"></Column>
        <Column field="description" header="Description" sortable style="width: 55%"></Column>
        <Column style="width: 20%" bodyStyle="text-align:right">
            <template #body="slotProps">
                <Button icon="pi pi-pencil" aria-label="Edit dictionary metadata" class="ml-2" rounded @click="onClickUpdateMetadata(slotProps.data)" />
                <Button icon="pi pi-file-edit" aria-label="Edit dictionary schema" class="ml-2" rounded @click="onClickUpdateFile(slotProps.data)" />
                <Button icon="pi pi-trash" aria-label="Delete dictionary" severity="danger" class="ml-2" rounded @click="onClickDelete(slotProps.data.id)" />
            </template>
        </Column>
    </DataTable>
</template>
