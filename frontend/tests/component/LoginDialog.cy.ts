import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import Dialog from 'primevue/dialog';
import DialogService from 'primevue/dialogservice';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import ToastService from 'primevue/toastservice';
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import LoginDialog from '../../src/components/LoginDialog.vue';
import ApiClientManager from '../../src/services/api-client.service';
import MessageService from '../../src/services/message.service';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

const mockLayoutState = {
  loginDialogVisible: ref(true)
};

function mountLoginDialog(props?) {
  return cy.mount(LoginDialog, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService],
      mocks: {
        t: (key) => key,
        layoutState: mockLayoutState
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
  beforeEach(() => {
    cy.spy(MessageService.prototype, 'messageSuccess').as('messageSuccessSpy');
    cy.spy(MessageService.prototype, 'messageError').as('messageErrorSpy');
    mockLayoutState.loginDialogVisible.value = true;
    mountLoginDialog();
  });

  it('should render the login dialog', () => {
    cy.get('[data-testid="login-dialog"]').should('exist');
  });

  it('should close the login dialog when the button is clicked', () => {
    cy.get('[data-testid="close-dialog-button"]')
      .click()
      .then(() => {
        mockLayoutState.loginDialogVisible.value = false;
        cy.get('[data-testid="login-dialog"]').should('not.exist');
      });
  });

  it('should handle form submission successfully', () => {
    const mockApiClient = {
      login: cy.stub().resolves({
        data: {
          status: 'OK',
          data: {
            access_token: 'mockAccessToken'
          }
        }
      })
    };
    cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
    mountLoginDialog();
    cy.get('[data-testid="input-username"]').type('correctusername');
    cy.get('[data-testid="input-password"]').type('correctpassword');
    cy.get('[data-testid="login-submit-button"]')
      .click()
      .then(() => {
        // Checks localStorage
        cy.window().then((win) => {
          expect(win.localStorage.getItem('token')).to.equal('mockAccessToken');
        });
        // Checks method calling
        cy.get('@messageSuccessSpy').should('have.been.called');
        // Controls the form reset
        cy.get('[data-testid="input-username"]').should('have.value', '');
        cy.get('[data-testid="input-password"]').should('have.value', '');
      });
  });

  it('should handle form submission failure', () => {
    const mockApiClient = {
      login: cy.stub().resolves({
        data: {
          status: 'BAD_CREDENTIAL',
          message: 'Invalid credentials'
        }
      })
    };
    cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
    mountLoginDialog();
    cy.get('[data-testid="input-username"]').type('wrongusername');
    cy.get('[data-testid="input-password"]').type('wrongpassword');
    cy.get('[data-testid="login-submit-button"]')
      .click()
      .then(() => {
        // Checks method calling
        cy.get('@messageErrorSpy').should('have.been.called');
        cy.get('[data-testid="login-dialog"]').should('exist');
      });
  });
});
