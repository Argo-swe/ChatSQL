<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  name: 'AppLogo',
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
  setup(props) {
    const logoSrc = computed(() => {
      return props.path.startsWith('/') ? process.env.BASE_URL + props.path : props.path;
    });

    return {
      logoSrc
    };
  }
});
</script>

<template>
  <img :src="logoSrc" alt="" :width="width" :height="height" class="logo" />
</template>

<style scoped>
.logo {
  cursor: pointer;
}
</style>
