// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import FileUpload from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import ToastService from 'primevue/toastservice';
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';
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

/**
 * Performs the mounting of the CreateUpdateDictionaryModal component.
 * @param mockDialogRef - A mock of the dialogRef object, containing the data passed from the parent object.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountCreateUpdateDictionaryModal(mockDialogRef, props?) {
  cy.spy(MessageService.prototype, 'messageSuccess').as('messageSuccessSpy');
  cy.spy(MessageService.prototype, 'messageError').as('messageErrorSpy');

  return cy.mount(CreateUpdateDictionaryModal, {
    global: {
      plugins: [i18n, PrimeVue, ToastService],
      mocks: {
        t: (key) => key
      },
      provide: {
        dialogRef: mockDialogRef
      },
      components: {
        PgButton: Button,
        PgInputText: InputText,
        PgFileUpload: FileUpload
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
      status: 'OK'
    }
  };
}

/**
 * Returns mock error response for the API call.
 */
function getFailureResponse() {
  return {
    data: {
      status: 'ERROR',
      message: 'Error while saving dictionary data'
    }
  };
}

/**
 * Mounts the CreateUpdateDictionaryModal component with a custom mock API client for dictionary creation.
 * @param response - The mock response to return.
 */
function mockCreateDictionary(response: any = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: true
    },
    close: () => true
  });
  const mockApiClient = {
    createDictionary: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.createDictionary).as('createDictionary');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  return mountCreateUpdateDictionaryModal(mockDialogRef);
}

/**
 * Mounts the CreateUpdateDictionaryModal component with a custom mock API client for dictionary metadata update.
 * @param response - The mock response to return.
 */
function mockUpdateDictionaryMetadata(response: any = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: false,
      dictionaryId: 1,
      dictionaryName: 'Orders',
      dictionaryDescription: 'Orders dictionary'
    },
    close: () => true
  });
  const mockApiClient = {
    updateDictionaryMetadata: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.updateDictionaryMetadata).as('updateDictionaryMetadata');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  return mountCreateUpdateDictionaryModal(mockDialogRef);
}

/**
 * Mounts the CreateUpdateDictionaryModal component with a custom mock API client for dictionary file update.
 * @param response - The mock response to return.
 */
function mockUpdateDictionaryFile(response: any = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: true,
      dictionaryId: 1
    },
    close: () => true
  });
  const mockApiClient = {
    updateDictionaryFile: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.updateDictionaryFile).as('updateDictionaryFile');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  return mountCreateUpdateDictionaryModal(mockDialogRef);
}

/**
 * Test suite for the CreateUpdateDictionaryModal component.
 */
describe('CreateUpdateDictionaryModal Component', () => {
  // Single and isolated test case
  it('should render the dictionary modal correctly', () => {
    mockCreateDictionary();
    cy.get('[data-testid="handle-dictionary-form"]').should('be.visible');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should handle dictionary creation successfully', () => {
    mockCreateDictionary();
    cy.get('[data-testid="dictionary-name-input"]').type('Orders');
    cy.get('[data-testid="dictionary-description-input"]').type('Orders dictionary');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json');

    cy.get('[data-testid="dictionary-submit-button"]').should('be.enabled').click();
    cy.get('@messageSuccessSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle dictionary creation failure', () => {
    mockCreateDictionary(getFailureResponse());
    cy.get('[data-testid="dictionary-name-input"]').type('Orders');
    cy.get('[data-testid="dictionary-description-input"]').type('Orders dictionary');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should disable the submit button when dictionary name is invalid', () => {
    mockUpdateDictionaryMetadata();
    cy.get('[data-testid="dictionary-name-input"]').type('***');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should disable the submit button when file format is invalid', () => {
    mockUpdateDictionaryFile();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.txt');

    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should handle dictionary metadata update successfully', () => {
    mockUpdateDictionaryMetadata();
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('New dictionary description');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('@messageSuccessSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle dictionary metadata update failure', () => {
    mockUpdateDictionaryMetadata(getFailureResponse());
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('Name already exists');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle dictionary file update successfully', () => {
    mockUpdateDictionaryFile();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('@messageSuccessSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle dictionary file update failure', () => {
    mockUpdateDictionaryFile(getFailureResponse());
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should clear the selected file', () => {
    mockUpdateDictionaryFile();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json');

    cy.get('[data-testid="dictionary-file-upload"]').find('input[type="file"]').should('not.exist');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.enabled');
    cy.get('[data-testid="clear-file-button"]').should('exist').click();
    cy.get('[data-testid="dictionary-file-upload"]').find('input[type="file"]').should('exist');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });
});
