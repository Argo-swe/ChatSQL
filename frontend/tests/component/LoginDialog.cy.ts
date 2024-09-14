// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import Dialog from 'primevue/dialog';
import DialogService from 'primevue/dialogservice';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import LoginDialog from '@/components/LoginDialog.vue';
import { useLayout } from '@/composables/layout';
import ApiClientManager from '@/services/api-client.service';
import MessageService from '@/services/message.service';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

const { layoutState } = useLayout();
let originalLoginDialogVisibleValue: boolean;

/**
 * Performs the mounting of the LoginDialog component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountLoginDialog(props?) {
  return cy.mount(LoginDialog, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService],
      mocks: {
        t: (key) => key
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

/**
 * Returns a successful mock response for the API call.
 */
function getSuccessResponse() {
  return {
    data: {
      status: 'OK',
      data: {
        access_token: 'mockAccessToken'
      }
    }
  };
}

/**
 * Returns mock error response for the API call.
 */
function getFailureResponse() {
  return {
    data: {
      status: 'BAD_CREDENTIAL',
      message: 'Invalid credentials'
    }
  };
}

/**
 * Mounts the LoginDialog component with a custom mock API client for authentication.
 * @param response - The mock response to return.
 */
function mockLogin(response: any = getSuccessResponse()) {
  const mockApiClient = {
    login: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.login).as('login');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  return mountLoginDialog(mockApiClient);
}

/**
 * Test suite for the LoginDialog component.
 */
describe('LoginDialog Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    cy.spy(MessageService.prototype, 'messageSuccess').as('messageSuccessSpy');
    cy.spy(MessageService.prototype, 'messageError').as('messageErrorSpy');
    originalLoginDialogVisibleValue = layoutState.loginDialogVisible.value;
    layoutState.loginDialogVisible.value = true;
    mountLoginDialog();
  });

  // Hook that runs after each test
  afterEach(() => {
    layoutState.loginDialogVisible.value = originalLoginDialogVisibleValue;
  });

  // Single and isolated test case
  it('should render the login dialog', () => {
    cy.get('[data-testid="login-dialog"]').should('exist');
  });

  // Single and isolated test case
  it('should close the login dialog when the button is clicked', () => {
    cy.get('[data-testid="close-dialog-button"]').should('exist').click();
    cy.get('[data-testid="login-dialog"]').should('not.exist');
  });

  // Single and isolated test case
  it('should handle form submission successfully', () => {
    mockLogin();
    cy.get('[data-testid="input-username"]').type('correctusername');
    cy.get('[data-testid="input-password"]').type('correctpassword');
    cy.get('[data-testid="login-submit-button"]').click();

    cy.get('@messageSuccessSpy').should('have.been.called');
    cy.get('[data-testid="login-dialog"]').should('not.exist');
    cy.window().then((win) => {
      expect(win.localStorage.getItem('token')).to.equal('mockAccessToken');
      layoutState.loginDialogVisible.value = true;
    });
    cy.get('[data-testid="input-username"]').should('have.value', '');
    cy.get('[data-testid="input-password"]').should('have.value', '');
  });

  // Single and isolated test case
  it('should handle form submission failure', () => {
    mockLogin(getFailureResponse());
    cy.get('[data-testid="input-username"]').type('wrongusername');
    cy.get('[data-testid="input-password"]').type('wrongpassword');
    cy.get('[data-testid="login-submit-button"]').click();

    cy.get('@messageErrorSpy').should('have.been.called');
    cy.get('[data-testid="login-dialog"]').should('exist');
  });
});
