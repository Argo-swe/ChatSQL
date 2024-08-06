import { messageService } from '@/services/message.service';
import type { Components } from '@/types/openapi';
import type { DictionaryMgmtMessages } from '@/types/wrapper';
import { useI18n } from 'vue-i18n';
import { useSharedState } from './shared-state';

const { t } = useI18n();
const { messageSuccess, messageError } = messageService();
const { dictionaryName, dictionaryId } = useSharedState();

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is created.
 */
const onCreateMessages: DictionaryMgmtMessages = {
  OK: () => t('actions.create.success'),
  BAD_REQUEST: () => `${t('actions.create.error')}\n${t('actions.formatError')}`,
  CONFLICT: () =>
    `${t('actions.create.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName })}`,
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
    `${t('actions.update.error')}\n${t('actions.notFoundById', { item: t('dictionary.title'), id: dictionaryId })}`,
  CONFLICT: () =>
    `${t('actions.update.error')}\n${t('actions.alreadyExistsByName', { item: t('dictionary.title'), name: dictionaryName })}`,
  DEFAULT: (message?: string | null) => `${t('actions.update.error')}\n${message}`
};

/**
 * Handles messages based on the response status.
 * @function handleStatusMex
 * @description This function determines which message to display and passes it to the appropriate message service.
 * @param messageHeader - A string representing the header for the message.
 * @param statusMessages - An object that maps status codes to functions which generate the message strings.
 * @param status - (Optional) The response status code.
 * @param defaultMessage - (Optional) An additional message to be appended.
 */
const handleStatusMex = (
  messageHeader: string,
  statusMessages: DictionaryMgmtMessages,
  status?: Components.Schemas.ResponseStatusEnum,
  message?: string | null
) => {
  const getMessage =
    status && statusMessages[status] ? statusMessages[status] : statusMessages['DEFAULT'];
  const statusMessage = getMessage ? getMessage(message) : '';
  if (status == 'OK') {
    messageSuccess(t(messageHeader), statusMessage);
  } else {
    messageError(t(messageHeader), statusMessage);
  }
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
    handleStatusMex
  };
}
