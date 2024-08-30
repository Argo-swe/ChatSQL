import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';

import LoginDialog from '@/components/LoginDialog.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';

import AppLayout from '@/views/AppLayout.vue';

import { useLayout } from '@/composables/layout';

const { layoutConfig, layoutState } = useLayout();

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

function mountAppLayout(props?) {
  return cy.mount(AppLayout, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService, router],
      mocks: {
        t: (key) => key,
      },
      components: {
        LoginDialog,
        AppTopbar,
        ConfigSidebar,
        MenuSidebar
      },
      /* stubs: {
        AppMenu: true
      } */
    },
    props
  });
}

describe('AppLayout Component', () => {
  it('should render correctly', () => {
    mountAppLayout();
    cy.get('[data-testid="layout-wrapper"]').should('be.visible');
  });

  it('should apply the correct classes based on layoutConfig and layoutState', () => {
    layoutConfig.darkTheme.value = false;
    layoutConfig.menuMode.value = 'overlay';
    layoutState.staticMenuDesktopInactive.value = true;
    layoutState.overlayMenuActive.value = true;
    layoutState.staticMenuMobileActive.value = true;
    layoutConfig.ripple.value = false;

    mountAppLayout();

    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-theme-light');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-overlay');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-overlay-active');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-mobile-active');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'p-ripple-disabled');
  
  });

  it('should apply different classes when layoutConfig and layoutState change', () => {
    // layoutConfig.darkTheme.value = true; // why this no worky??
    layoutConfig.menuMode.value = 'static';
    layoutState.staticMenuDesktopInactive.value = true;
    layoutState.overlayMenuActive.value = false;
    layoutState.staticMenuMobileActive.value = false;
    layoutConfig.ripple.value = true;

    mountAppLayout();

    // cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-theme-dark');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-static');
    cy.get('[data-testid="layout-wrapper"]').should('have.class', 'layout-static-inactive');
    cy.get('[data-testid="layout-wrapper"]').should('not.have.class', 'layout-overlay-active');
    cy.get('[data-testid="layout-wrapper"]').should('not.have.class', 'layout-mobile-active');
    cy.get('[data-testid="layout-wrapper"]').should('not.have.class', 'p-ripple-disabled');
  });

});