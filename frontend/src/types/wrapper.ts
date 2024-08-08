import type { ComputedRef } from 'vue';
import type { Components } from './openapi';

/**
 * Type representing the dictionary preview data structure.
 * @type {DictionaryPreviewDto} DictionaryPreview
 */
export type DictionaryPreview = Components.Schemas.DictionaryPreviewDto;

/**
 * Base options for configuring a message.
 * @interface BaseMessageOptions
 * @property {String} message - (Optional) An additional message to be appended.
 */
export interface BaseMessageOptions {
  message?: string | null;
}

/**
 * Interface representing options for dictionary status messages.
 * @interface DictionaryMessageOptions
 * @property {Number} dictionaryId - (Optional) The ID of the dictionary.
 * @property {String} dictionaryName - (Optional) The name of the dictionary.
 */
export interface DictionaryMessageOptions extends BaseMessageOptions {
  dictionaryId?: number | null;
  dictionaryName?: string | null;
}

/**
 * Interface representing options for login status messages.
 * @interface LoginMessageOptions
 * @property {String} username - (Optional) The username of the user.
 */
export interface LoginMessageOptions extends BaseMessageOptions {
  username?: string | null;
}

/**
 * Type representing a dictionary of status messages.
 */
export type StatusMessages<TOptions extends BaseMessageOptions> = {
  [key in Components.Schemas.ResponseStatusEnum]?: (options?: TOptions) => string;
} & {
  DEFAULT: (options?: TOptions) => string;
};

/**
 * Interface representing a message object.
 * @interface MessageWrapper
 * @property {String} message - The content of the message.
 * @property {Boolean} isSent - A flag indicating whether the message has been sent or received by the user.
 */
export interface MessageWrapper {
  message: string;
  isSent: boolean;
}

/**
 * Interface representing a menu item.
 * @interface MenuItem
 * @property {ComputedRef} label - A computed label for the menu item.
 * @property {String} icon - The CSS class for the icon.
 * @property {String} to - The URL path or route the menu item links to.
 */
export interface MenuItem {
  label: ComputedRef<string>;
  icon: string;
  to: string;
}

/**
 * Interface representing a menu section that can contain multiple menu items.
 * @interface MenuWrapper
 * @property {ComputedRef} label - (Optional) A computed label for the menu section.
 * @property {Array} items - (Optional) An array of menu items.
 * @property {boolean} separator - (Optional) A flag indicating whether a section is a separator.
 */
export interface MenuWrapper {
  label?: ComputedRef<string>;
  items?: MenuItem[];
  separator?: boolean;
}

/**
 * Type representing the menu structure.
 * @type {MenuWrapper[]} Menu
 */
export type Menu = MenuWrapper[];

/**
 * Interface representing a map of strings (CSS class names) to boolean values.
 * @interface CSSClasses
 * @description This type of declaration is especially useful when working with objects that represent conditional CSS classes.
 */
export interface CSSClasses {
  [key: string]: boolean;
}
