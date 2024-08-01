<script setup lang="ts">
import { useLayout } from '@/composables/layout';
import AuthService from '@/services/auth.service';
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import AppLogo from '@/components/AppLogo.vue';

import { useConfirm } from 'primevue/useconfirm';
const confirm = useConfirm();

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const { onMenuToggle, layoutState } = useLayout();

const router = useRouter();

let isLogged = ref(AuthService.isLogged());

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);

onMounted(() => {
  bindOutsideClickListener();
  window.addEventListener('token-localstorage-changed', () => {
    isLogged.value = AuthService.isLogged();
  });
});

onBeforeUnmount(() => {
  unbindOutsideClickListener();
});

const onTopBarMenuButton = () => {
  topbarMenuActive.value = !topbarMenuActive.value;
};
const onSettingsClick = () => {
  topbarMenuActive.value = false;
  layoutState.configSidebarVisible.value = !layoutState.configSidebarVisible.value;
};
const onLoginClick = () => {
  topbarMenuActive.value = false;
  layoutState.loginDialogVisible.value = !layoutState.loginDialogVisible.value;
};
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
const topbarMenuClasses = computed(() => {
  return {
    'layout-topbar-menu-mobile-active': topbarMenuActive.value
  };
});

const bindOutsideClickListener = () => {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event) => {
      if (isOutsideClicked(event)) {
        topbarMenuActive.value = false;
      }
    };
    document.addEventListener('click', outsideClickListener.value);
  }
};
const unbindOutsideClickListener = () => {
  if (outsideClickListener.value) {
    document.removeEventListener('click', outsideClickListener);
    outsideClickListener.value = null;
  }
};
const isOutsideClicked = (event) => {
  if (!topbarMenuActive.value) return;

  const sidebarEl = document.querySelector('.layout-topbar-menu');
  const topbarEl = document.querySelector('.layout-topbar-menu-button');

  return !(
    sidebarEl.isSameNode(event.target) ||
    sidebarEl.contains(event.target) ||
    topbarEl.isSameNode(event.target) ||
    topbarEl.contains(event.target)
  );
};
</script>

<template>
  <div class="layout-topbar">
    <router-link to="/" class="layout-topbar-logo">
      <app-logo></app-logo>
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
