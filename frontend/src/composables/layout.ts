import { computed, reactive, toRefs } from 'vue';

// Reactive object to hold the layout configuration settings
const layoutConfig = reactive({
  ripple: true,
  darkTheme: localStorage.getItem('darkTheme') === 'true',
  inputStyle: 'outlined',
  menuMode: 'static',
  theme: 'aura-light-blue',
  scale: parseInt(localStorage.getItem('scale') ?? '14'),
  activeMenuItem: null
});

// Reactive object to hold the layout state
const layoutState = reactive({
  staticMenuDesktopInactive: false,
  overlayMenuActive: false,
  profileSidebarVisible: false,
  configSidebarVisible: false,
  staticMenuMobileActive: false,
  menuHoverActive: false,
  loginDialogVisible: false
});

/**
 * Computed property to determine if the sidebar is active.
 */
const isSidebarActive = computed(
  () => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive
);

/**
 * Computed property to determine if the dark theme is enabled.
 */
const isDarkTheme = computed(() => layoutConfig.darkTheme);

/**
 * Sets the active menu item in the layout configuration.
 * @param item - The menu item to set as active.
 */
const setActiveMenuItem = (item: any) => {
  layoutConfig.activeMenuItem = item.value || item;
};

/**
 * Sets the scale value in the layout configuration and stores it in localStorage.
 * @param scale - The new scale value to set.
 */
const setScale = (scale: number) => {
  layoutConfig.scale = scale;
  localStorage.setItem('scale', scale.toString());
};

/**
 * Toggles the state of the menu based on the current menu mode and window width.
 */
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

/**
 * Composable function to expose layout-related state and methods.
 */
export function useLayout() {
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
