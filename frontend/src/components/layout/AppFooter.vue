<script setup lang="ts">
import { computed } from 'vue';

import { useI18n } from 'vue-i18n'
const { t } = useI18n();

const logoUrl = computed(() => {
    return `/layout/images/argo_trasparente.svg`;
});
</script>

<template>
    <div class="layout-footer w-full">
        <div class="titolo">
            <img :src="logoUrl" alt="Logo" height="40" class="argo-logo mr-2" />
            <!-- <span class="font-medium ml-2">{{ t('footer.title') }}</span> -->
        </div>
        <p class="copyright">© {{ new Date().getFullYear() }} {{ t('footer.copyright.title') }}<br>{{ t('footer.copyright.section') }}</p>
    </div>
</template>
<style lang="scss" scoped></style>
