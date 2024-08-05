<script setup lang="ts">
// External libraries
import { useConfirm } from 'primevue/useconfirm';
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

// Internal dependencies
import { useCheckOutsideClick } from '@/composables/check-click';
import { useLayout } from '@/composables/layout';
import AuthService from '@/services/auth.service';

// Child Components
import AppLogo from '@/components/AppLogo.vue';

const router = useRouter();
const confirm = useConfirm();
const { t } = useI18n();
const { onMenuToggle, layoutState } = useLayout();
const { isOutsideClicked } = useCheckOutsideClick([
  '.layout-topbar-menu',
  '.layout-topbar-menu-button'
]);
const outsideClickListener = ref<((event: Event) => void) | null>(null);
const topbarMenuActive = ref(false);
let isLogged = ref(AuthService.isLogged());

onMounted(() => {
  bindOutsideClickListener();
  window.addEventListener('token-localstorage-changed', () => {
    isLogged.value = AuthService.isLogged();
  });
});

onBeforeUnmount(() => {
  unbindOutsideClickListener();
});

/**
 * Binds a click event listener to the document to detect clicks outside a specific area.
 * @function unbindOutsideClickListener
 * @description This arrow function will toggle the visibility of the topbar menu when a click outside is detected.
 */
const bindOutsideClickListener = () => {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event: Event) => {
      if (topbarMenuActive.value && isOutsideClicked(event)) {
        topbarMenuActive.value = false;
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

/**
 * Toggles the visibility state of the topbar menu
 * @function onTopBarMenuButton
 */
const onTopBarMenuButton = () => {
  topbarMenuActive.value = !topbarMenuActive.value;
};

/**
 * Toggles the CSS class for the mobile menu.
 */
const topbarMenuClasses = computed(() => {
  return {
    'layout-topbar-menu-mobile-active': topbarMenuActive.value
  };
});

/**
 * Toggles the visibility of the config sidebar and closes the topbar menu.
 * @function onSettingsClick
 */
const onSettingsClick = () => {
  topbarMenuActive.value = false;
  layoutState.configSidebarVisible.value = !layoutState.configSidebarVisible.value;
};

/**
 * Toggles the visibility of the login dialog and closes the topbar menu.
 * @function onLoginClick
 */
const onLoginClick = () => {
  topbarMenuActive.value = false;
  layoutState.loginDialogVisible.value = !layoutState.loginDialogVisible.value;
};

/**
 * Shows a confirmation dialog and performs the logout action if accepted.
 * @function onLogoutClick
 */
const onLogoutClick = () => {
  confirm.require({
    message: t('general.confirm.proceed'),
    header: t('text.Logout'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('text.Yes'),
    rejectLabel: t('text.No'),
    accept: () => {
      AuthService.logout();
      router.push('/');
    }
  });
};
</script>

<template>
  <div class="layout-topbar">
    <router-link to="/" class="layout-topbar-logo">
      <app-logo path="icons/argo_icona.svg" height="40"></app-logo>
      <span>ChatSQL</span>
    </router-link>

    <button
      class="p-link layout-menu-button layout-topbar-button"
      :aria-label="t('general.menu.openMainNavMenu')"
      @click="onMenuToggle()"
    >
      <i class="pi pi-bars"></i>
    </button>

    <button
      class="p-link layout-topbar-menu-button layout-topbar-button"
      :aria-label="t('text.toggle_menu')"
      @click="onTopBarMenuButton()"
    >
      <i class="pi pi-ellipsis-v"></i>
    </button>

    <div id="option-menu" class="layout-topbar-menu" :class="topbarMenuClasses">
      <button
        class="p-link layout-topbar-button"
        :title="t('text.Settings')"
        :aria-label="t('text.Settings')"
        @click="onSettingsClick()"
      >
        <i class="pi pi-cog"></i><span>{{ t('text.Settings') }}</span>
      </button>
      <button
        v-if="!isLogged"
        class="p-link layout-topbar-button"
        :title="t('text.Login')"
        :aria-label="t('text.Login')"
        @click="onLoginClick()"
      >
        <i class="pi pi-user"></i><span>{{ t('text.Login') }}</span>
      </button>
      <button
        v-else
        class="p-link layout-topbar-button"
        :title="t('text.Logout')"
        :aria-label="t('text.Logout')"
        @click="onLogoutClick()"
      >
        <i class="pi pi-sign-out"></i><span>{{ t('text.Logout') }}</span>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#option-menu.layout-topbar-menu button span {
  display: none;
}

@media (max-width: 991px) {
  #option-menu.layout-topbar-menu button span {
    display: block;
  }
}
</style>
