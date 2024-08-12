<script setup lang="ts">
// External libraries
import { computed, ref, watch, type ComputedRef } from 'vue';

// Internal dependencies
import { useCheckOutsideClick } from '@/composables/check-click';
import { useLayout } from '@/composables/layout';
import type { CSSClasses } from '@/types/wrapper';

// Child Components
import LoginDialog from '@/components/LoginDialog.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';

const { layoutConfig, layoutState, isSidebarActive } = useLayout();
const { isOutsideClicked } = useCheckOutsideClick(['.layout-sidebar', '.layout-menu-button']);
const outsideClickListener = ref<((event: Event) => void) | null>(null);

/**
 * Binds a click event listener to the document to detect clicks outside a specific area.
 * @function bindOutsideClickListener
 */
const bindOutsideClickListener = () => {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event: Event) => {
      if (isOutsideClicked(event)) {
        layoutState.overlayMenuActive.value = false;
        layoutState.staticMenuMobileActive.value = false;
        layoutState.menuHoverActive.value = false;
      }
    };
    document.addEventListener('click', outsideClickListener.value);
  }
};

/**
 * Removes the click event listener from the document and resets the listener reference to null.
 *  @function unbindOutsideClickListener
 */
const unbindOutsideClickListener = () => {
  if (outsideClickListener.value) {
    document.removeEventListener('click', outsideClickListener.value);
    outsideClickListener.value = null;
  }
};

// Toggles the binding of the outside click listener based on sidebar state.
watch(isSidebarActive, (newVal) => {
  if (newVal) {
    bindOutsideClickListener();
  } else {
    unbindOutsideClickListener();
  }
});

/**
 * Computes the dynamic CSS classes to be applied to the container element based on the
 * current layout and theme configurations.
 */
const containerClass: ComputedRef<CSSClasses> = computed(() => {
  return {
    'layout-theme-light': layoutConfig.darkTheme.value === false,
    'layout-theme-dark': layoutConfig.darkTheme.value === true,
    'layout-overlay': layoutConfig.menuMode.value === 'overlay',
    'layout-static': layoutConfig.menuMode.value === 'static',
    'layout-static-inactive':
      layoutState.staticMenuDesktopInactive.value && layoutConfig.menuMode.value === 'static',
    'layout-overlay-active': layoutState.overlayMenuActive.value,
    'layout-mobile-active': layoutState.staticMenuMobileActive.value,
    'p-ripple-disabled': layoutConfig.ripple.value === false
  };
});
</script>

<template>
  <div class="layout-wrapper" :class="containerClass">
    <app-topbar></app-topbar>
    <login-dialog />
    <div class="layout-sidebar">
      <menu-sidebar></menu-sidebar>
    </div>
    <div class="layout-main-container">
      <div class="layout-main">
        <router-view></router-view>
      </div>
    </div>
    <config-sidebar></config-sidebar>
    <PgScrollTop />
    <div class="layout-mask"></div>
  </div>
  <PgToast position="bottom-right" />
</template>
