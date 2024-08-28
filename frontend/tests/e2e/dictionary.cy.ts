/**
 * Test suite for dictionary management requirements.
 */
describe('Dictionary Management', () => {
  // Hook that runs once before all tests
  before(() => {
    cy.visit('/');
    cy.setupDictionary();
  });

  // Hook that runs once after all tests
  after(() => {
    cy.cleanupDictionary();
  });

  // Hook that runs before each test
  beforeEach(() => {
    cy.handleSession().then(() => {
      cy.visit('/dictionary');
    });
  });

  // Test case
  it('verify that the admin can update dictionary name', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('System Test Orders 2');

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the system returns an error if the dictionary name is bad formatted', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('***');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the admin can update dictionary description', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('New test description');

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the admin can update dictionary file', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-file-button"]').click();
    });
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/cinema.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the admin can download dictionary file', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="download-file-button"]').click();
    });
    const filename = 'cypress/downloads/system_test_orders_2_schema.json';
    cy.readFile(filename, { timeout: 15000 }).should('exist');
  });
});
