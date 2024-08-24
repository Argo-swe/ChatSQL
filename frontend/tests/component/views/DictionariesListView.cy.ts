import Button from 'primevue/button';
import Column from 'primevue/column';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DataTable from 'primevue/datatable';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';
import CreateUpdateDictionaryModal from '../../../src/components/CreateUpdateDictionaryModal.vue';
import ApiClientManager from '../../../src/services/api-client.service';
import MessageService from '../../../src/services/message.service';
import UtilsService from '../../../src/services/utils.service';
import DictionariesListView from '../../../src/views/DictionariesListView.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountDictionariesListView(mockApiClient, props?) {
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
        CreateUpdateDictionaryModal
      }
    },
    props
  });
}

function getGlobalMockApiClient() {
  return {
    getAllDictionaries: cy.stub().resolves({
      data: {
        status: 'OK',
        data: [
          {
            id: 0,
            name: 'Orders',
            description: 'Orders dictionary'
          }
        ]
      }
    }),
    getDictionaryFile: cy.stub().resolves({
      data: 'File content'
    })
  };
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
      message: 'Error while deleting dictionary'
    }
  };
}

function mockDeleteDictionary(response = getSuccessResponse()) {
  const mockApiClient = {
    ...getGlobalMockApiClient(),
    deleteDictionary: cy.stub().resolves(response)
  };
  return mountDictionariesListView(mockApiClient);
}

describe('DictionariesListView Component', () => {
  it('should render the dictionaries list correctly', () => {
    mountDictionariesListView(getGlobalMockApiClient());
    cy.get('[data-testid="dictionary-page-header"]').should('be.visible');
    cy.get('[data-testid="dictionaries-table"]').should('be.visible');
  });

  it('shows dictionary modal when clicking the add button', () => {
    mountDictionariesListView(getGlobalMockApiClient()).then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="dictionary-create-button"]')
        .should('exist')
        .click()
        .then(() => {
          expect(openDialogSpy).to.be.called;

          let callArgs = openDialogSpy.getCall(0).args[0];
          expect(callArgs).to.equal(CreateUpdateDictionaryModal);
          callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(true);
        });
    });
  });

  it('shows dictionary modal when clicking the update metadata button', () => {
    mountDictionariesListView(getGlobalMockApiClient()).then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="update-metadata-button"]')
        .first()
        .should('exist')
        .click()
        .then(() => {
          expect(openDialogSpy).to.be.called;

          let callArgs = openDialogSpy.getCall(0).args[0];
          expect(callArgs).to.equal(CreateUpdateDictionaryModal);
          callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(false);
          expect(callArgs.data.dictionaryId).to.equal(0);
          expect(callArgs.data.dictionaryName).to.equal('Orders');
          expect(callArgs.data.dictionaryDescription).to.equal('Orders dictionary');
        });
    });
  });

  it('shows dictionary modal when clicking the update file button', () => {
    mountDictionariesListView(getGlobalMockApiClient()).then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="update-file-button"]')
        .first()
        .should('exist')
        .click()
        .then(() => {
          expect(openDialogSpy).to.be.called;

          let callArgs = openDialogSpy.getCall(0).args[0];
          expect(callArgs).to.equal(CreateUpdateDictionaryModal);
          callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.withFile).to.equal(true);
          expect(callArgs.data.dictionaryId).to.equal(0);
        });
    });
  });

  it('should trigger file download with correct message', () => {
    cy.spy(UtilsService, 'downloadFile').as('downloadFileSpy');
    mountDictionariesListView(getGlobalMockApiClient());
    cy.get('[data-testid="download-file-button"]').first().should('exist').click();

    cy.get('@downloadFileSpy').should('have.been.calledWith', 'orders_schema.json', 'File content');
  });

  it('should handle dictionary deletion successfully', () => {
    mockDeleteDictionary().then(({ component }) => {
      cy.stub(component.confirm, 'require').callsFake((options) => {
        options.accept();
      });
    });
    cy.get('[data-testid="dictionary-delete-button"]').should('exist').click();
    cy.get('@messageSuccessSpy').should('have.been.called');
  });

  it('should handle dictionary deletion failure', () => {
    mockDeleteDictionary(getFailureResponse()).then(({ component }) => {
      cy.stub(component.confirm, 'require').callsFake((options) => {
        options.accept();
      });
    });
    cy.get('[data-testid="dictionary-delete-button"]').should('exist').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });
});
