import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import { createI18n } from 'vue-i18n';
import LoginDialog from '../../src/components/LoginDialog.vue';
/* import { useLayout } from '../../src/composables/layout'; */
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';

import BadgeDirective from 'primevue/badgedirective';
import Ripple from 'primevue/ripple';
import StyleClass from 'primevue/styleclass';
import Tooltip from 'primevue/tooltip';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountLoginDialog(props?) {
  /* const useLayoutMock = () => ({
    layoutState: {
      loginDialogVisible: false
    }
  }); */

  return cy.mount(LoginDialog, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService],
      directives: [BadgeDirective, Ripple, StyleClass, Tooltip],
      mocks: {
        t: (key) => key,
        layoutState: {
          loginDialogVisible: true
        }
      },
      components: {
        PgButton: Button,
        PgInputText: InputText,
        PgPassword: Password,
        PgDialog: Dialog
      }
    },
    props
  });
}

describe('LoginDialog Component', () => {
  it('should render', () => {
    mountLoginDialog();
    cy.get('[data-testid="login-dialog"]').should('exist');
  });
});
