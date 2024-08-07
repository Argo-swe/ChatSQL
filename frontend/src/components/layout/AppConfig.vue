<script setup lang="ts">
import { useLayout } from '@/composables/layout';
import { usePrimeVue } from 'primevue/config';
import { onMounted, ref } from 'vue';

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

const onChangeTheme = (theme: string, mode: boolean) => {
  $primevue.changeTheme(layoutConfig.theme.value, theme, 'theme-css', () => {
    layoutConfig.theme.value = theme;
    layoutConfig.darkTheme.value = mode;
  });
  localStorage.setItem('darkTheme', mode.toString());
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

const onDarkModeChange = (value: boolean) => {
  const newThemeName = value
    ? layoutConfig.theme.value.replace('light', 'dark')
    : layoutConfig.theme.value.replace('dark', 'light');

  layoutConfig.darkTheme.value = value;
  onChangeTheme(newThemeName, value);
};

const onLanguageChange = (value: string) => {
  localStorage.setItem('language', value);
};

onMounted(() => {
  onDarkModeChange(layoutConfig.darkTheme.value);
  applyScale();
});
</script>

<template>
  <PgSidebar
    v-model:visible="layoutState.configSidebarVisible.value"
    position="right"
    class="layout-config-sidebar w-26rem"
    pt:close-button="ml-auto"
  >
    <div class="p-2">
      <section
        class="pb-4 flex align-items-center justify-content-between border-bottom-1 surface-border"
      >
        <span class="text-xl font-semibold">{{ t(`settings.scale`) }}</span>
        <div
          class="flex align-items-center gap-2 border-1 surface-border py-1 px-2"
          style="border-radius: 30px"
        >
          <PgButton
            icon="pi pi-minus"
            text
            rounded
            :disabled="layoutConfig.scale.value === scales[0]"
            @click="decrementScale"
          />
          <i
            v-for="s in scales"
            :key="s"
            :class="[
              'pi pi-circle-fill text-sm text-200',
              { 'text-lg text-primary': s === layoutConfig.scale.value }
            ]"
          />

          <PgButton
            icon="pi pi-plus"
            text
            rounded
            :disabled="layoutConfig.scale.value === scales[scales.length - 1]"
            @click="incrementScale"
          />
        </div>
      </section>

      <section
        class="py-4 flex align-items-center justify-content-between border-bottom-1 surface-border"
      >
        <span class="text-xl font-semibold">{{ t(`settings.darkMode`) }}</span>
        <PgInputSwitch
          :model-value="layoutConfig.darkTheme.value"
          @update:model-value="onDarkModeChange"
        />
      </section>

      <section
        class="py-4 flex align-items-center justify-content-between border-bottom-1 surface-border"
      >
        <span class="text-xl font-semibold">{{ t(`settings.language`) }}</span>
        <PgDropdown
          v-model="locale"
          :options="supportedLocales"
          @update:model-value="onLanguageChange"
        >
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
        </PgDropdown>
      </section>
    </div>
  </PgSidebar>
</template>
