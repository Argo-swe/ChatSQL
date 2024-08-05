import type { Components } from '@/types/openapi';
import type { ComputedRef } from 'vue';

/**
 * Type representing the dictionary preview data structure.
 * @type {DictionaryPreviewDto} DictionaryPreview
 */
export type DictionaryPreview = Components.Schemas.DictionaryPreviewDto;

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
