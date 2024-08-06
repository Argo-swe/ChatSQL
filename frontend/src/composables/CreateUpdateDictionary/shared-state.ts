import { ref } from 'vue';

// Shared reactive variables
const dictionaryId = ref();
const dictionaryName = ref('');

/**
 * Sets the value of the dictionaryId reactive variable.
 * @param dictId - The dictionary ID to be set.
 */
const setDictionaryId = (dictId: number) => {
  dictionaryId.value = dictId;
};

/**
 * Sets the value of the dictionaryName reactive variable.
 * @param dictName - The dictionary name to be set.
 */
const setDictionaryName = (dictName: string) => {
  dictionaryName.value = dictName;
};

/**
 * Provides access to the reactive variables and their setter functions.
 */
export function useSharedState() {
  return {
    dictionaryName,
    dictionaryId,
    setDictionaryName,
    setDictionaryId
  };
}
