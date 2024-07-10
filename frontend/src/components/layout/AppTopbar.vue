<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/components/layout/composables/layout';
import { useRouter } from 'vue-router';
import AuthService from '@/services/auth.service';

import { useConfirm } from "primevue/useconfirm";
const confirm = useConfirm();

import { useI18n } from 'vue-i18n'
const { t } = useI18n();

const { layoutConfig, onMenuToggle, layoutState } = useLayout();

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

const logoUrl = computed(() => {
    return `/layout/images/argo_icona.svg`;
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
            router.push('/')
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

    return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target));
};
</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img :src="logoUrl" alt="Logo" class="argo-logo" />
            <span>ChatSQL</span>
        </router-link>

        <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()" :aria-label="t('general.menu.openMainNavMenu')">
            <i class="pi pi-bars"></i>
        </button>

        <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()" :aria-label="t('text.toggle_menu')">
            <i class="pi pi-ellipsis-v"></i>
        </button>

        <div id="option-menu" class="layout-topbar-menu" :class="topbarMenuClasses">
            <button @click="onSettingsClick()" class="p-link layout-topbar-button" :title="t('text.Settings')" :aria-label="t('text.Settings')">
                <i class="pi pi-cog"></i><span>{{ t('text.Settings') }}</span>
            </button>
            <button v-if="!isLogged" @click="onLoginClick()" class="p-link layout-topbar-button" :title="t('text.Login')" :aria-label="t('text.Login')">
                <i class="pi pi-user"></i><span>{{ t('text.Login') }}</span>
            </button>
            <button v-else @click="onLogoutClick()" class="p-link layout-topbar-button" :title="t('text.Logout')" :aria-label="t('text.Logout')">
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
