import type { Components } from '@/types/openapi';
import type {
  BaseMessageOptions,
  DictionaryMessageOptions,
  LoginMessageOptions,
  StatusMessages
} from '@/types/wrapper';
import i18n from '../main';

/**
 * Provides access to the `t` function from VueI18n for translating messages.
 * @function getI18n
 * @description Required for using VueI18n outside of a component.
 */
function getI18n() {
  return i18n.global.t;
}

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is created.
 */
const onCreateMessages: StatusMessages<DictionaryMessageOptions> = {
  OK: () => getI18n()('actions.create.success'),
  BAD_REQUEST: () => `${getI18n()('actions.create.error')}\n${getI18n()('actions.formatError')}`,
  CONFLICT: ({ dictionaryName }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.create.error')}\n${getI18n()('actions.alreadyExistsByName', { item: getI18n()('dictionary.title'), name: dictionaryName })}`,
  DEFAULT: ({ message }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.create.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is updated.
 */
const onUpdateMessages: StatusMessages<DictionaryMessageOptions> = {
  OK: () => getI18n()('actions.update.success'),
  BAD_REQUEST: () => `${getI18n()('actions.update.error')}\n${getI18n()('actions.formatError')}`,
  NOT_FOUND: ({ dictionaryId }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.update.error')}\n${getI18n()('actions.notFoundById', { item: getI18n()('dictionary.title'), id: dictionaryId })}`,
  CONFLICT: ({ dictionaryName }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.update.error')}\n${getI18n()('actions.alreadyExistsByName', { item: getI18n()('dictionary.title'), name: dictionaryName })}`,
  DEFAULT: ({ message }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.update.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when one or more data dictionaries are retrieved.
 */
const onRetrieveMessages: StatusMessages<DictionaryMessageOptions> = {
  NOT_FOUND: ({ dictionaryId }: DictionaryMessageOptions = {}) =>
    `${getI18n()('general.list.error')}\n${getI18n()('actions.notFoundById', { item: getI18n()('dictionary.title'), id: dictionaryId })}`,
  DEFAULT: ({ message }: DictionaryMessageOptions = {}) =>
    `${getI18n()('general.list.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the data dictionary is deleted.
 */
const onDeleteMessages: StatusMessages<DictionaryMessageOptions> = {
  OK: () => getI18n()('actions.delete.success'),
  NOT_FOUND: ({ dictionaryId }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.delete.error')}\n${getI18n()('actions.notFoundById', { item: getI18n()('dictionary.title'), id: dictionaryId })}`,
  DEFAULT: ({ message }: DictionaryMessageOptions = {}) =>
    `${getI18n()('actions.delete.error')}\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when the user logs in.
 */
const onLoginMessages: StatusMessages<LoginMessageOptions> = {
  OK: ({ username }: LoginMessageOptions = {}) => getI18n()('login.success', { name: username }),
  NOT_FOUND: ({ username }: LoginMessageOptions = {}) =>
    getI18n()('actions.notFoundByName', { item: getI18n()('text.User'), name: username }),
  BAD_CREDENTIAL: () => getI18n()('login.badCredential'),
  DEFAULT: ({ message }: LoginMessageOptions = {}) =>
    `${getI18n()('text.genericError')}:\n${message}`
};

/**
 * List of messages associated with a status code.
 * Triggered when prompt or debug messages are generated.
 */
const onGenerateMessages: StatusMessages<BaseMessageOptions> = {
  BAD_REQUEST: () => `${getI18n()('actions.generate.error')}\n${getI18n()('actions.formatError')}`,
  DEFAULT: ({ message }: BaseMessageOptions = {}) =>
    `${getI18n()('actions.generate.error')}\n${message}`
};

/**
 * Generates messages based on the response status.
 * @function getStatusMex
 * @description This function determines which message to display and passes it to the appropriate message service.
 * @param statusMessages - An object that maps status codes to functions which generate the message strings.
 * @param status - (Optional) The response status code.
 * @param options - (Optional) An object containing options for message generation.
 */
const getStatusMex = <TOptions extends BaseMessageOptions>(
  statusMessages: StatusMessages<TOptions>,
  status?: Components.Schemas.ResponseStatusEnum,
  options?: TOptions
) => {
  const getMessage =
    status && statusMessages[status] ? statusMessages[status] : statusMessages['DEFAULT'];
  const statusMessage = getMessage(options);
  return statusMessage;
};

/**
 * Define a mapping of message types to their corresponding message handlers.
 */
const messagesCrudMap = {
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
      messagesCrudMap[type] || messagesCrudMap['create'],
    onLoginMessages,
    onGenerateMessages,
    getStatusMex
  };
}
