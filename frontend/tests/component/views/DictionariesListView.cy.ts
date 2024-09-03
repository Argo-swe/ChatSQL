// External dependencies
import Button from 'primevue/button';
import Column from 'primevue/column';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DataTable from 'primevue/datatable';
import DialogService from 'primevue/dialogservice';
import InputText from 'primevue/inputtext';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import CreateUpdateDictionaryModal from '@/components/CreateUpdateDictionaryModal.vue';
import ApiClientManager from '@/services/api-client.service';
import MessageService from '@/services/message.service';
import UtilsService from '@/services/utils.service';
import DictionariesListView from '@/views/DictionariesListView.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the DictionariesListView component.
 * @param mockApiClient - The mock API client that replaces the real API client to simulate calls.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountDictionariesListView(mockApiClient: any = getGlobalMockApiClient(), props?) {
  cy.spy(MessageService.prototype, 'messageSuccess').as('messageSuccessSpy');
  cy.spy(MessageService.prototype, 'messageError').as('messageErrorSpy');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);

  return cy.mount(DictionariesListView, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService],
      mocks: {
        t: (key) => key
      },
      components: {
        PgButton: Button,
        PgDataTable: DataTable,
        PgColumn: Column,
        PgInputText: InputText,
        CreateUpdateDictionaryModal
      }
    },
    props
  });
}

/**
 * Returns a global mock API client with stubs that simulate API calls.
 */
function getGlobalMockApiClient() {
  const globalMockApiClient = {
    getAllDictionaries: cy.stub().resolves({
      data: {
        status: 'OK',
        data: [
          {
            id: 1,
            name: 'Orders',
            description: 'Orders dictionary'
          },
          {
            id: 2,
            name: 'Test name',
            description: 'Test description'
          }
        ]
      }
    }),
    getDictionaryFile: cy.stub().resolves({
      data: 'File content'
    })
  };
  cy.wrap(globalMockApiClient.getAllDictionaries).as('getAllDictionaries');
  cy.wrap(globalMockApiClient.getDictionaryFile).as('getDictionaryFile');
  return globalMockApiClient;
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
      message: 'Error while deleting dictionary'
    }
  };
}

/**
 * Mounts the DictionariesListView component with a custom mock API client for dictionary deletion.
 * @param response - The mock response to return.
 */
function mockDeleteDictionary(response: any = getSuccessResponse()) {
  const mockApiClient = {
    ...getGlobalMockApiClient(),
    deleteDictionary: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.deleteDictionary).as('deleteDictionary');
  return mountDictionariesListView(mockApiClient);
}

/**
 * Verifies that the call heard by the spy invoked the CreateUpdateDictionaryModal component.
 */
function CheckSubComponentCall() {
  cy.get('@openDialogSpy').should('have.been.called');
  cy.get('@openDialogSpy').its('firstCall.args[0]').should('equal', CreateUpdateDictionaryModal);
}

/**
 * Checks the result of a successful search.
 */
function checkSuccessfulSearch() {
  cy.contains('Orders').should('not.exist');
  cy.contains('Test name').should('exist');
}

/**
 * Checks the result of an empty search.
 */
function checkEmptySearch() {
  cy.contains('general.list.empty').should('exist');
}

/**
 * Test suite for the DictionariesListView component.
 */
describe('DictionariesListView Component', () => {
  // Single and isolated test case
  it('should render the dictionaries list correctly', () => {
    mountDictionariesListView();
    cy.get('[data-testid="dictionary-page-header"]').should('be.visible');
    cy.get('[data-testid="dictionaries-table"]').should('be.visible');
  });

  // Single and isolated test case
  it('should handle search by name successfully', () => {
    mountDictionariesListView();
    cy.get('[data-testid="search-by-name"]').type('Test name');
    checkSuccessfulSearch();
  });

  // Single and isolated test case
  it('should handle search by name failure', () => {
    mountDictionariesListView();
    cy.get('[data-testid="search-by-name"]').type('Cinema');
    checkEmptySearch();
  });

  // Single and isolated test case
  it('should handle search by description successfully', () => {
    mountDictionariesListView();
    cy.get('[data-testid="search-by-description"]').type('Test description');
    checkSuccessfulSearch();
  });

  // Single and isolated test case
  it('should handle search by description failure', () => {
    mountDictionariesListView();
    cy.get('[data-testid="search-by-description"]').type('Gym');
    checkEmptySearch();
  });

  // Single and isolated test case
  it('shows dictionary modal when clicking the add button', () => {
    mountDictionariesListView().then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="dictionary-create-button"]')
        .should('exist')
        .click()
        .then(() => {
          CheckSubComponentCall();
          const callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(true);
        });
    });
  });

  // Single and isolated test case
  it('shows dictionary modal when clicking the update metadata button', () => {
    mountDictionariesListView().then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="update-metadata-button"]')
        .first()
        .should('exist')
        .click()
        .then(() => {
          CheckSubComponentCall();
          const callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(false);
          expect(callArgs.data.dictionaryId).to.equal(1);
          expect(callArgs.data.dictionaryName).to.equal('Orders');
          expect(callArgs.data.dictionaryDescription).to.equal('Orders dictionary');
        });
    });
  });

  // Single and isolated test case
  it('shows dictionary modal when clicking the update file button', () => {
    mountDictionariesListView().then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="update-file-button"]')
        .first()
        .should('exist')
        .click()
        .then(() => {
          CheckSubComponentCall();
          const callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(true);
          expect(callArgs.data.dictionaryId).to.equal(1);
        });
    });
  });

  // Single and isolated test case
  it('should trigger file download with correct message', () => {
    cy.spy(UtilsService, 'downloadFile').as('downloadFileSpy');
    mountDictionariesListView();
    cy.get('[data-testid="download-file-button"]').first().should('exist').click();
    cy.get('@downloadFileSpy').should('have.been.calledWith', 'orders_schema.json', 'File content');
  });

  // Single and isolated test case
  it('should handle dictionary deletion successfully', () => {
    mockDeleteDictionary().then(({ component }) => {
      cy.stub(component.confirm, 'require').callsFake((options) => {
        options.accept();
      });
    });
    cy.get('[data-testid="dictionary-delete-button"]').first().should('exist').click();
    cy.get('@messageSuccessSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle dictionary deletion failure', () => {
    mockDeleteDictionary(getFailureResponse()).then(({ component }) => {
      cy.stub(component.confirm, 'require').callsFake((options) => {
        options.accept();
      });
    });
    cy.get('[data-testid="dictionary-delete-button"]').first().should('exist').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });
});
