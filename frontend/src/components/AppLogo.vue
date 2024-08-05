<script setup lang="ts">
// External libraries
import { computed, type ComputedRef } from 'vue';

// Internal dependencies
import { useLayout } from '@/composables/layout';
import type { CSSClasses } from '@/types/wrapper';

/**
 * Props for AppLogo component.
 */
withDefaults(
  defineProps<{
    /**
     * @prop {String} path
     * @description The URL or path to the image.
     */
    path: string;
    /**
     * @prop {String} [width='auto']
     * @description The width of the image. Default is 'auto'.
     */
    width: string;
    /**
     * @prop {String} [height='auto']
     * @description The height of the image. Default is 'auto'.
     */
    height: string;
  }>(),
  {
    width: 'auto',
    height: 'auto'
  }
);

const { isDarkTheme } = useLayout();

/**
 * Computed property that returns an object with CSS classes based on the current theme.
 * @type {CSSClasses}
 * @property {Boolean} 'logo-dark-theme-filter' - True if the theme is dark, otherwise false.
 */
const logoClass: ComputedRef<CSSClasses> = computed(() => ({
  'logo-dark-theme-filter': isDarkTheme.value
}));
</script>

<template>
  <img :src="path" alt="" :width="width" :height="height" :class="logoClass" />
</template>

<style scoped>
.logo-dark-theme-filter {
  filter: invert(100%);
}
</style>
