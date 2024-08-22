import PrimeVue from 'primevue/config';
import { createI18n } from 'vue-i18n';
import ConfigSidebar from '../../../src/components/layout/ConfigSidebar.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountConfigSidebar(props?) {
  return cy.mount(ConfigSidebar, {
    global: {
      plugins: [i18n, PrimeVue],
      mocks: {
        t: (key) => key,
        layoutState: {
          configSidebarVisible: {
            value: true
          }
        },
        layoutConfig: {
          scale: {
            value: 1
          },
          theme: {
            value: 'aura-light-blue'
          },
          darkTheme: {
            value: false
          }
        }
      }
    },
    props
  });
}

describe('ConfigSidebar Component', () => {
  it('should display correctly', () => {
    mountConfigSidebar();

    cy.get('.layout-config-sidebar').should('be.visible');
  });

  it('should change scale on scale button press', () => {
    mountConfigSidebar();

    cy.get('[data-test-id="increase-scale"]').click();
  });
});
