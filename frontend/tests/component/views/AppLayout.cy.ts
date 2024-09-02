// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import Dialog from 'primevue/dialog';
import DialogService from 'primevue/dialogservice';
import Sidebar from 'primevue/sidebar';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

// Internal dependencies
import LoginDialog from '@/components/LoginDialog.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';
import { useLayout } from '@/composables/layout';
import AppLayout from '@/views/AppLayout.vue';
import DictionariesListView from '@/views/DictionariesListView.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

// Mock VueRouter
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

const { layoutConfig, layoutState } = useLayout();
let originalDarkThemeValue: boolean;
let originaMenuModeValue: string;
let originalStaticMenuDesktopInactiveValue: boolean;
let originalOverlayMenuActiveValue: boolean;
let originalStaticMenuMobileActiveValue: boolean;
let originalRippleValue: boolean;

/**
 * Performs the mounting of the AppLayout component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountAppLayout(props?) {
  return cy.mount(AppLayout, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService, router],
      mocks: {
        t: (key) => key
      },
      components: {
        AppTopbar,
        LoginDialog,
        MenuSidebar,
        ConfigSidebar,
        PgButton: Button,
        PgDialog: Dialog,
        PgSidebar: Sidebar,
        DictionariesListView
      }
    },
    props
  });
}

/**
 * Opens the main navigation menu.
 */
function openMainNavMenu() {
  cy.get('[data-testid="open-main-nav-menu-button"]').click();
  cy.get('[data-testid="menu-sidebar"]').should('be.visible');
}

/**
 * Test suite for the AppLayout component.
 */
describe('AppLayout Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    originalDarkThemeValue = layoutConfig.darkTheme.value;
    originaMenuModeValue = layoutConfig.menuMode.value;
    originalStaticMenuDesktopInactiveValue = layoutState.staticMenuDesktopInactive.value;
    originalOverlayMenuActiveValue = layoutState.overlayMenuActive.value;
    originalStaticMenuMobileActiveValue = layoutState.staticMenuMobileActive.value;
    originalRippleValue = layoutConfig.ripple.value;
    mountAppLayout();
  });

  // Hook that runs after each test
  afterEach(() => {
    layoutConfig.darkTheme.value = originalDarkThemeValue;
    layoutConfig.menuMode.value = originaMenuModeValue;
    layoutState.staticMenuDesktopInactive.value = originalStaticMenuDesktopInactiveValue;
    layoutState.overlayMenuActive.value = originalOverlayMenuActiveValue;
    layoutState.staticMenuMobileActive.value = originalStaticMenuMobileActiveValue;
    layoutConfig.ripple.value = originalRippleValue;
  });

  // Single and isolated test case
  it('should render correctly', () => {
    cy.get('[data-testid="global-layout-wrapper"]').should('be.visible');
  });

  // Single and isolated test case
  it('should apply the correct classes based on layoutConfig and layoutState', () => {
    layoutConfig.menuMode.value = 'overlay';
    layoutState.overlayMenuActive.value = true;
    layoutState.staticMenuMobileActive.value = true;
    layoutConfig.ripple.value = false;

    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-theme-light');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-overlay');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-overlay-active');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-mobile-active');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'p-ripple-disabled');
  });

  // Single and isolated test case
  it('should apply different classes when layoutConfig and layoutState change', () => {
    layoutConfig.darkTheme.value = true;
    layoutState.staticMenuDesktopInactive.value = true;

    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-theme-dark');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-static');
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-static-inactive');
    cy.get('[data-testid="global-layout-wrapper"]').should(
      'not.have.class',
      'layout-overlay-active'
    );
    cy.get('[data-testid="global-layout-wrapper"]').should(
      'not.have.class',
      'layout-mobile-active'
    );
    cy.get('[data-testid="global-layout-wrapper"]').should('not.have.class', 'p-ripple-disabled');
  });

  // Single and isolated test case
  it('should toggle login dialog on click event', () => {
    mountAppLayout();
    cy.get('[data-testid="login-button"]').click({ force: true });
    cy.get('[data-testid="login-dialog"]').should('be.visible');
    cy.get('[data-testid="close-dialog-button"]').click();
    cy.get('[data-testid="login-dialog"]').should('not.exist');
  });

  // Single and isolated test case
  it('should toggle config sidebar on click event', () => {
    cy.get('[data-testid="open-settings-button"]').click({ force: true });
    cy.get('[data-testid="config-sidebar"]').should('be.visible');
    cy.window().then((win) => {
      cy.get('body').click(win.innerWidth - 1, win.innerHeight - 1);
      cy.get('[data-testid="config-sidebar"]').should('not.exist');
    });
  });

  // Single and isolated test case
  it('should toggle menu sidebar on click event', () => {
    cy.viewport('iphone-x');
    openMainNavMenu();
    cy.get('[data-testid="close-menu-sidebar"]').click();
    cy.get('[data-testid="menu-sidebar"]').should('not.be.visible');
    openMainNavMenu();
    cy.window().then((win) => {
      cy.get('body').click(win.innerWidth - 1, win.innerHeight - 1);
      cy.get('[data-testid="menu-sidebar"]').should('not.be.visible');
    });
  });
});
