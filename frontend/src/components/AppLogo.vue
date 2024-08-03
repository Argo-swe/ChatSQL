<script lang="ts">
// External libraries
import { computed, defineComponent } from 'vue';

// Internal dependencies
import { useLayout } from '@/composables/layout';

export default defineComponent({
  name: 'AppLogo',
  /**
   * Props for AppLogo component.
   * @prop {String} path - The URL or path to the image.
   * @prop {String} [width='auto'] - The width of the image. Default is 'auto'.
   * @prop {String} [height='auto'] - The height of the image. Default is 'auto'.
   */
  props: {
    path: {
      type: String,
      required: true
    },
    width: {
      type: String,
      default: 'auto'
    },
    height: {
      type: String,
      default: 'auto'
    }
  },
  setup() {
    const { isDarkTheme } = useLayout();

    /**
     * Computed property that returns an object with a CSS class based on the current theme.
     * @type {Object}
     * @property {Boolean} 'logo-dark-theme-filter' - True if the theme is dark, otherwise false.
     */
    const logoClass = computed(() => ({
      'logo-dark-theme-filter': isDarkTheme.value
    }));

    return {
      logoClass
    };
  }
});
</script>

<template>
  <img :src="path" alt="" :width="width" :height="height" :class="logoClass" />
</template>

<style scoped>
.logo-dark-theme-filter {
  filter: invert(100%);
}
</style>
