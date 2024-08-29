import { ref } from 'vue';
import { createI18n } from 'vue-i18n';

import LoginDialog from '@/components/LoginDialog.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';

import AppLayout from '../../../src/views/AppLayout.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountAppLayout(props?) {
  return cy.mount(AppLayout, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key,
        layoutState: {
          configSidebarVisible: ref(true)
        }
      },
      components: {
        LoginDialog,
        AppTopbar,
        ConfigSidebar,
        MenuSidebar
      }
    },
    props
  });
}

describe('AppLayout Component', () => {
  it('should render correctly', () => {
    mountAppLayout();
    cy.get('[data-testid="app-layout"]').should('be.visible');
    
  });
});