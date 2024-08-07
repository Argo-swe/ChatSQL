import type { Components } from '@/types/openapi';
import type { DictStatusMessageOptions, DictionaryMgmtMessages } from '@/types/wrapper';
import i18n from '../main';

// Required for using VueI18n outside of a component
const { t } = i18n.global;

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is created.
 */
const onCreateMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.create.success'),
  BAD_REQUEST: () => `${t('actions.create.error')}\n${t('actions.formatError')}`,
  CONFLICT: ({ dictionaryName }: DictStatusMessageOptions = {}) =>
    `${t('actions.create.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName })}`,
  DEFAULT: ({ message }: DictStatusMessageOptions = {}) =>
    `${t('actions.create.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is updated.
 */
const onUpdateMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.update.success'),
  BAD_REQUEST: () => `${t('actions.update.error')}\n${t('actions.formatError')}`,
  NOT_FOUND: ({ dictionaryId }: DictStatusMessageOptions = {}) =>
    `${t('actions.update.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`,
  CONFLICT: ({ dictionaryName }: DictStatusMessageOptions = {}) =>
    `${t('actions.update.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName })}`,
  DEFAULT: ({ message }: DictStatusMessageOptions = {}) =>
    `${t('actions.update.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when one or more data dictionaries are retrieved.
 */
const onRetrieveMessages: DictionaryMgmtMessages = {
  NOT_FOUND: ({ dictionaryId }: DictStatusMessageOptions = {}) =>
    `${t('general.list.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`,
  DEFAULT: ({ message }: DictStatusMessageOptions = {}) => `${t('general.list.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is deleted.
 */
const onDeleteMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.delete.success'),
  NOT_FOUND: ({ dictionaryId }: DictStatusMessageOptions = {}) =>
    `${t('actions.delete.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`,
  DEFAULT: ({ message }: DictStatusMessageOptions = {}) =>
    `${t('actions.delete.error')}\n${message}`
};

/**
 * Generates messages based on the response status.
 * @function getStatusMex
 * @description This function determines which message to display and passes it to the appropriate message service.
 * @param statusMessages - An object that maps status codes to functions which generate the message strings.
 * @param status - (Optional) The response status code.
 * @param options - (Optional) An object containing options for message generation.
 */
const getStatusMex = (
  statusMessages: DictionaryMgmtMessages,
  status?: Components.Schemas.ResponseStatusEnum,
  options?: DictStatusMessageOptions
) => {
  const getMessage =
    status && statusMessages[status] ? statusMessages[status] : statusMessages['DEFAULT'];
  const statusMessage = getMessage(options);
  return statusMessage;
};

/**
 * Define a mapping of message types to their corresponding message handlers.
 */
const messagesMap = {
  create: onCreateMessages,
  read: onRetrieveMessages,
  update: onUpdateMessages,
  delete: onDeleteMessages
};

/**
 * Composable function to provide message handling utilities.
 */
export function useMessages() {
  return {
    getMessages: (type: 'create' | 'read' | 'update' | 'delete') =>
      messagesMap[type] || messagesMap['create'],
    getStatusMex
  };
}
