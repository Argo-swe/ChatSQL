<script setup lang="ts">
// External libraries
import { computed, ref, watch } from 'vue';

// Internal dependencies
import { useCheckOutsideClick } from '@/composables/check-click';
import { useLayout } from '@/composables/layout';

// Child Components
import LoginDialog from '@/components/LoginDialog.vue';
import AppConfig from '@/components/layout/AppConfig.vue';
import AppSidebar from '@/components/layout/AppSidebar.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';

const { layoutConfig, layoutState, isSidebarActive } = useLayout();
const { isOutsideClicked } = useCheckOutsideClick(['.layout-sidebar', '.layout-menu-button']);
const outsideClickListener = ref<((event: Event) => void) | null>(null);

watch(isSidebarActive, (newVal) => {
  if (newVal) {
    bindOutsideClickListener();
  } else {
    unbindOutsideClickListener();
  }
});

const containerClass = computed(() => {
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

const bindOutsideClickListener = () => {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event: MouseEvent) => {
      if (isOutsideClicked(event)) {
        layoutState.overlayMenuActive.value = false;
        layoutState.staticMenuMobileActive.value = false;
        layoutState.menuHoverActive.value = false;
      }
    };
    document.addEventListener('click', outsideClickListener.value);
  }
};

const unbindOutsideClickListener = () => {
  if (outsideClickListener.value) {
    document.removeEventListener('click', outsideClickListener.value);
    outsideClickListener.value = null;
  }
};
</script>

<template>
  <div class="layout-wrapper" :class="containerClass">
    <app-topbar></app-topbar>
    <login-dialog />
    <div class="layout-sidebar">
      <app-sidebar></app-sidebar>
    </div>
    <div class="layout-main-container">
      <div class="layout-main">
        <router-view></router-view>
      </div>
    </div>
    <app-config></app-config>
    <PgScrollTop />
    <div class="layout-mask"></div>
  </div>
  <PgToast position="bottom-right" />
</template>
