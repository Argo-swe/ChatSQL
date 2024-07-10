<script setup lang="ts">
import { computed, ref} from 'vue';

import { useI18n } from 'vue-i18n'
const { t } = useI18n();

const version = ref(import.meta.env.VITE_VERSION ?? null);

const logoUrl = computed(() => {
    return `/layout/images/argo_trasparente.svg`;
});
</script>

<template>
    <div class="layout-footer w-full">
        <div class="titolo">
            <img :src="logoUrl" alt="Logo" height="40" class="argo-logo mr-2" />
        </div>
        <p class="copyright">
            <strong v-if="version"> v{{ version }} </strong>
            <span>© {{ new Date().getFullYear() }} {{ t('footer.copyright.title') }}</span>
            <span>{{ t('footer.copyright.section') }}</span>
        </p>
    </div>
</template>
<style lang="scss" scoped></style>
