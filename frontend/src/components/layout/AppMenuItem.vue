<script setup lang="ts">
// External libraries
import { onBeforeMount, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

// Internal dependencies
import { useLayout } from '@/composables/layout';

/**
 * Props for AppMenuItem component.
 */
const props = withDefaults(
  defineProps<{
    /**
     * @prop {Any} item
     * @description Object representing a menu item.
     */
    item: any;
    /**
     * @prop {Number} index
     * @description Index of the menu item.
     */
    index: number;
    /**
     * @prop {Boolean} root
     * @description Flag indicating whether the menu item is the root of the navigation menu.
     */
    root: boolean;
    /**
     * @prop {String | null} parentItemKey
     * @description Key to identify the parent menu item.
     */
    parentItemKey: string | null;
  }>(),
  {
    item: () => ({}),
    index: 0,
    root: true,
    parentItemKey: null
  }
);

const route = useRoute();
const { layoutConfig, layoutState, setActiveMenuItem, onMenuToggle } = useLayout();
const isActiveMenu = ref(false);
const itemKey = ref<string | null>(null);

onBeforeMount(() => {
  itemKey.value = props.parentItemKey
    ? props.parentItemKey + '-' + props.index
    : String(props.index);

  const activeItem = layoutConfig.activeMenuItem.value as string | null;

  isActiveMenu.value =
    activeItem === itemKey.value ||
    (activeItem ? activeItem.startsWith(itemKey.value + '-') : false);
});

// Watches for changes to the active menu item and updates the `isActiveMenu` reactive property accordingly.
watch(
  () => layoutConfig.activeMenuItem.value,
  (newVal: string | null) => {
    isActiveMenu.value =
      newVal === itemKey.value || (newVal ? newVal.startsWith(itemKey.value + '-') : false);
  }
);

/**
 * Checks if the current route path matches the specified path.
 * @param item - The menu item containing the route path to check against.
 */
const checkActiveRoute = (item: any) => {
  return route.path === item.to;
};

/**
 * Toggles the menu visibility if the clicked item has a navigation property and any of the menus are active.
 */
const handleMenuToggle = (item: any) => {
  const { overlayMenuActive, staticMenuMobileActive } = layoutState;

  if ((item.to || item.url) && (staticMenuMobileActive.value || overlayMenuActive.value)) {
    onMenuToggle();
  }
};

/**
 * Updates the currently active menu item based on the clicked item.
 */
const updateActiveMenuItem = (item: any) => {
  let foundItemKey;

  if (item.items) {
    foundItemKey = isActiveMenu.value ? props.parentItemKey : itemKey;
  } else {
    foundItemKey = itemKey.value;
  }

  setActiveMenuItem(foundItemKey);
};

/**
 * Handles the click event for a menu item, applying various actions based on the item's properties.
 */
const itemClick = (event: Event, item: any) => {
  if (item.disabled) {
    event.preventDefault();
    return;
  }

  handleMenuToggle(item);

  if (item.command) {
    item.command({ originalEvent: event, item: item });
  }

  updateActiveMenuItem(item);
};
</script>

<template>
  <li :class="{ 'layout-root-menuitem': root, 'active-menuitem': isActiveMenu }">
    <div v-if="root && item.visible !== false" class="layout-menuitem-root-text">
      {{ item.label }}
    </div>
    <!-- External link or clickable item to open a sub-menu -->
    <a
      v-if="(!item.to || item.items) && item.visible !== false"
      :href="item.url"
      :class="item.class"
      :target="item.target"
      tabindex="0"
      @click="itemClick($event, item)"
    >
      <i :class="item.icon" class="layout-menuitem-icon"></i>
      <span class="layout-menuitem-text">{{ item.label }}</span>
      <i v-if="item.items" class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
    </a>
    <!-- Internal navigation link (managed by Vue Router) -->
    <router-link
      v-if="item.to && !item.items && item.visible !== false"
      :class="[item.class, { 'active-route': checkActiveRoute(item) }]"
      tabindex="0"
      :to="item.to"
      @click="itemClick($event, item)"
    >
      <i :class="item.icon" class="layout-menuitem-icon"></i>
      <span class="layout-menuitem-text">{{ item.label }}</span>
      <i v-if="item.items" class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
    </router-link>
    <!-- Sub menu with transition -->
    <Transition v-if="item.items && item.visible !== false" name="layout-submenu">
      <ul v-show="root ? true : isActiveMenu" class="layout-submenu">
        <app-menu-item
          v-for="(child, i) in item.items"
          :key="child"
          :index="i"
          :item="child"
          :parent-item-key="itemKey"
          :root="false"
        ></app-menu-item>
      </ul>
    </Transition>
  </li>
</template>
