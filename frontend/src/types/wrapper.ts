import type { Components } from '@/types/openapi';

/**
 * Type representing the dictionary preview data structure.
 * @type DictionaryPreview
 */
export type DictionaryPreview = Components.Schemas.DictionaryPreviewDto;

/**
 * Interface representing a message object.
 * @interface MessageWrapper
 * @property {string} message - The content of the message.
 * @property {boolean} isSent - A flag indicating whether the message has been sent or received by the user.
 */
export interface MessageWrapper {
  message: string;
  isSent: boolean;
}
