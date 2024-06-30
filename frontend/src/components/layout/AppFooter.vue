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
            <img :src="logoUrl" alt="Logo" height="40" class="mr-2" />
            <!-- <span class="font-medium ml-2">{{ t('general.groupName') }}</span> -->
        </div>
        <p class="copyright">© {{ new Date().getFullYear() }} {{ t('general.groupName') }}<br>{{ t('general.copyright') }}</p>
    </div>
</template>
<style lang="scss" scoped></style>
