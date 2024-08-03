import { computed, reactive, toRefs } from 'vue';

const layoutConfig = reactive({
  ripple: true,
  darkTheme: localStorage.getItem('darkTheme') === 'true',
  inputStyle: 'outlined',
  menuMode: 'static',
  theme: 'aura-light-blue',
  scale: parseInt(localStorage.getItem('scale') ?? '14'),
  activeMenuItem: null
});

const layoutState = reactive({
  staticMenuDesktopInactive: false,
  overlayMenuActive: false,
  profileSidebarVisible: false,
  configSidebarVisible: false,
  staticMenuMobileActive: false,
  menuHoverActive: false,
  loginDialogVisible: false
});

export function useLayout() {
  const setScale = (scale: number) => {
    layoutConfig.scale = scale;
    localStorage.setItem('scale', scale.toString());
  };

  const setActiveMenuItem = (item: any) => {
    layoutConfig.activeMenuItem = item.value || item;
  };

  const onMenuToggle = () => {
    if (layoutConfig.menuMode === 'overlay') {
      layoutState.overlayMenuActive = !layoutState.overlayMenuActive;
    }

    if (window.innerWidth > 991) {
      layoutState.staticMenuDesktopInactive = !layoutState.staticMenuDesktopInactive;
    } else {
      layoutState.staticMenuMobileActive = !layoutState.staticMenuMobileActive;
    }
  };

  const isSidebarActive = computed(
    () => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive
  );

  const isDarkTheme = computed(() => layoutConfig.darkTheme);

  return {
    layoutConfig: toRefs(layoutConfig),
    layoutState: toRefs(layoutState),
    setScale,
    onMenuToggle,
    isSidebarActive,
    isDarkTheme,
    setActiveMenuItem
  };
}
