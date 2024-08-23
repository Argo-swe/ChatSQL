import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import FileUpload from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import ToastService from 'primevue/toastservice';
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import CreateUpdateDictionaryModal from '../../src/components/CreateUpdateDictionaryModal.vue';
import ApiClientManager from '../../src/services/api-client.service';
import MessageService from '../../src/services/message.service';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

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

function getSuccessResponse() {
  return {
    data: {
      status: 'OK'
    }
  };
}

function getFailureResponse() {
  return {
    data: {
      status: 'ERROR',
      message: 'Error while saving dictionary data'
    }
  };
}

function mockCreateDictionary(response = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: true
    },
    close: () => true
  });
  const mockApiClient = {
    createDictionary: cy.stub().resolves(response)
  };
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  mountCreateUpdateDictionaryModal(mockDialogRef);
}

function mockUpdateDictionaryMetadata(response = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: false,
      dictionaryId: 0,
      dictionaryName: 'Orders',
      dictionaryDescription: 'Orders dictionary'
    },
    close: () => true
  });
  const mockApiClient = {
    updateDictionaryMetadata: cy.stub().resolves(response)
  };
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  mountCreateUpdateDictionaryModal(mockDialogRef);
}

function mockUpdateDictionaryFile(response = getSuccessResponse()) {
  const mockDialogRef = ref({
    data: {
      withFile: true,
      dictionaryId: 0
    },
    close: () => true
  });
  const mockApiClient = {
    updateDictionaryFile: cy.stub().resolves(response)
  };
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);
  mountCreateUpdateDictionaryModal(mockDialogRef);
}

describe('CreateUpdateDictionaryModal Component', () => {
  it('should render the dictionary modal', () => {
    mockCreateDictionary();
    cy.get('[data-testid="handle-dictionary-form"]').should('be.visible');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });

  it('should handle dictionary creation successfully', () => {
    mockCreateDictionary();
    cy.get('[data-testid="dictionary-name-input"]').type('Orders');
    cy.get('[data-testid="dictionary-description-input"]').type('Orders dictionary');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageSuccessSpy').should('have.been.called');
      });
  });

  it('should handle dictionary creation failure', () => {
    mockCreateDictionary(getFailureResponse());
    cy.get('[data-testid="dictionary-name-input"]').type('Orders');
    cy.get('[data-testid="dictionary-description-input"]').type('Orders dictionary');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageErrorSpy').should('have.been.called');
      });
  });

  it('should disable the submit button when file format is invalid', () => {
    mockUpdateDictionaryFile();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.txt');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
  });

  it('should handle dictionary metadata update successfully', () => {
    mockUpdateDictionaryMetadata();
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('New dictionary description');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageSuccessSpy').should('have.been.called');
      });
  });

  it('should handle dictionary metadata update failure', () => {
    mockUpdateDictionaryMetadata(getFailureResponse());
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('***');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageErrorSpy').should('have.been.called');
      });
  });

  it('should handle dictionary file update successfully', () => {
    mockUpdateDictionaryFile();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageSuccessSpy').should('have.been.called');
      });
  });

  it('should handle dictionary file update failure', () => {
    mockUpdateDictionaryFile(getFailureResponse());
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json');

    cy.get('[data-testid="dictionary-submit-button"]')
      .click()
      .then(() => {
        cy.get('@messageErrorSpy').should('have.been.called');
      });
  });

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
