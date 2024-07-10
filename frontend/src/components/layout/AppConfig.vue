<script setup lang="ts">
import { ref, computed } from 'vue';
import { onMounted } from 'vue';
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '@/components/layout/composables/layout';

import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

defineProps({
    simple: {
        type: Boolean,
        default: false
    }
});

const $primevue = usePrimeVue();

const scales = ref([12, 13, 14, 15, 16]);
const supportedLocales = ref(['it', 'en']);

const { setScale, layoutConfig, layoutState } = useLayout();

const onChangeTheme = (theme, mode) => {
    $primevue.changeTheme(layoutConfig.theme.value, theme, 'theme-css', () => {
        layoutConfig.theme.value = theme;
        layoutConfig.darkTheme.value = mode;
    });
    localStorage.setItem('darkTheme', mode);
};
const decrementScale = () => {
    setScale(layoutConfig.scale.value - 1);
    applyScale();
};
const incrementScale = () => {
    setScale(layoutConfig.scale.value + 1);
    applyScale();
};
const applyScale = () => {
    document.documentElement.style.fontSize = layoutConfig.scale.value + 'px';
};
const onDarkModeChange = (value) => {
    const newThemeName = value ? layoutConfig.theme.value.replace('light', 'dark') : layoutConfig.theme.value.replace('dark', 'light');

    layoutConfig.darkTheme.value = value;
    onChangeTheme(newThemeName, value);
};
const onLanguageChange = (value) => {
    localStorage.setItem('language', value);
};
const changeTheme = (theme, color) => {
    let newTheme, dark;

    newTheme = theme + '-' + (layoutConfig.darkTheme.value ? 'dark' : 'light');

    if (color) {
        newTheme += '-' + color;
    }

    if (newTheme.startsWith('md-') && compactMaterial.value) {
        newTheme = newTheme.replace('md-', 'mdc-');
    }

    dark = layoutConfig.darkTheme.value;

    onChangeTheme(newTheme, dark);
};
const isThemeActive = (themeFamily, color) => {
    let themeName;
    let themePrefix = themeFamily === 'md' && compactMaterial.value ? 'mdc' : themeFamily;

    themeName = themePrefix + (layoutConfig.darkTheme.value ? '-dark' : '-light');

    if (color) {
        themeName += '-' + color;
    }

    return layoutConfig.theme.value === themeName;
};

onMounted(() => {
    onDarkModeChange(layoutConfig.darkTheme.value);
    applyScale();
});

</script>

<template>
    <Sidebar v-model:visible="layoutState.configSidebarVisible.value" position="right" class="layout-config-sidebar w-26rem" pt:closeButton="ml-auto">
        <div class="p-2">
            <section class="pb-4 flex align-items-center justify-content-between border-bottom-1 surface-border">
                <span class="text-xl font-semibold">{{ t(`settings.scale`) }}</span>
                <div class="flex align-items-center gap-2 border-1 surface-border py-1 px-2" style="border-radius: 30px">
                    <Button icon="pi pi-minus" @click="decrementScale" text rounded :disabled="layoutConfig.scale.value === scales[0]" />
                    <i v-for="s in scales" :key="s" :class="['pi pi-circle-fill text-sm text-200', { 'text-lg text-primary': s === layoutConfig.scale.value }]" />

                    <Button icon="pi pi-plus" @click="incrementScale" text rounded :disabled="layoutConfig.scale.value === scales[scales.length - 1]" />
                </div>
            </section>

            <section class="py-4 flex align-items-center justify-content-between border-bottom-1 surface-border">
                <span class="text-xl font-semibold">{{ t(`settings.darkMode`) }}</span>
                <InputSwitch :modelValue="layoutConfig.darkTheme.value" @update:modelValue="onDarkModeChange" />
            </section>

            <section class="py-4 flex align-items-center justify-content-between border-bottom-1 surface-border">
                <span class="text-xl font-semibold">{{ t(`settings.language`) }}</span>
                <Dropdown v-model="locale" :options="supportedLocales"
                     @update:modelValue="onLanguageChange">
                    <template #value="slotProps">
                        <div class="capitalize">
                            {{ t(`locale.${slotProps.value}`) }}
                        </div>
                    </template>
                    <template #option="slotProps">
                        <div class="capitalize">
                            {{ t(`locale.${slotProps.option}`) }}
                        </div>
                    </template>
                </Dropdown>
            </section>
        </div>
    </Sidebar>
</template>

<style lang="scss" scoped></style>
