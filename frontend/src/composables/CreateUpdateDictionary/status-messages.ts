import type { Components } from '@/types/openapi';
import type { DictionaryMgmtMessages } from '@/types/wrapper';
import i18n from '../../main';
import { useSharedState } from './shared-state';

// Required for using VueI18n outside of a component
const { t } = i18n.global;
const { dictionaryName, dictionaryId } = useSharedState();

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is created.
 */
const onCreateMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.create.success'),
  BAD_REQUEST: () => `${t('actions.create.error')}\n${t('actions.formatError')}`,
  CONFLICT: () =>
    `${t('actions.create.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName.value })}`,
  DEFAULT: (message?: string | null) => `${t('actions.create.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is updated.
 */
const onUpdateMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.update.success'),
  BAD_REQUEST: () => `${t('actions.update.error')}\n${t('actions.formatError')}`,
  NOT_FOUND: () =>
    `${t('actions.update.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId.value })}`,
  CONFLICT: () =>
    `${t('actions.update.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName.value })}`,
  DEFAULT: (message?: string | null) => `${t('actions.update.error')}\n${message}`
};

/**
 * Generates messages based on the response status.
 * @function getStatusMex
 * @description This function determines which message to display and passes it to the appropriate message service.
 * @param statusMessages - An object that maps status codes to functions which generate the message strings.
 * @param status - (Optional) The response status code.
 * @param defaultMessage - (Optional) An additional message to be appended.
 */
const getStatusMex = (
  statusMessages: DictionaryMgmtMessages,
  status?: Components.Schemas.ResponseStatusEnum,
  message?: string | null
) => {
  const getMessage =
    status && statusMessages[status] ? statusMessages[status] : statusMessages['DEFAULT'];
  const statusMessage = getMessage(message);
  return statusMessage;
};

/**
 * Define a mapping of message types to their corresponding message handlers.
 */
const messagesMap = {
  create: onCreateMessages,
  update: onUpdateMessages
};

/**
 * Composable function to provide message handling utilities.
 */
export function useMessages() {
  return {
    getMessages: (type: 'create' | 'update') => messagesMap[type] || messagesMap['create'],
    getStatusMex
  };
}
