/**
 * Test suite for dictionary management requirements.
 */
describe('Dictionary Management', () => {
  // Hook that runs once before all tests
  before(() => {
    cy.visit('/');
    // Verify that the admin can insert a new data dictionary
    cy.setupDictionary().then(() => {
      cy.logout();
    });
  });

  // Hook that runs once after all tests
  after(() => {
    // Verify that the admin can delete a dictionary
    cy.cleanupDictionary();
    cy.logout();
  });

  // Hook that runs before each test
  beforeEach(() => {
    cy.handleSession().then(() => {
      cy.visit('/dictionary');
    });
  });

  // Test case
  it('verify that the admin can view the list of dictionaries with related information', () => {
    cy.get('[data-testid="dictionaries-table"]').should('be.visible');
  });

  // Test case
  it('verify that the admin can update dictionary name', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('System test orders 2');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-success').should('exist');
    cy.contains('System test orders 2').should('exist');
  });

  // Test case
  it('verify that the admin can update dictionary description', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('New system test description');

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-success').should('exist');
    cy.contains('New system test description').should('exist');
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
    cy.get('[data-testid="toast-message"]', { timeout: 15000 })
      .find('.p-toast-message-success')
      .should('exist');
  });

  // Test case
  it('verify that the system returns an error if the dictionary name is bad formatted', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('***');

    cy.get('[data-testid="dictionary-name-input"]').invoke('removeAttr', 'invalid');
    cy.get('[data-testid="dictionary-submit-button"]').invoke('removeAttr', 'disabled');
    cy.get('[data-testid="dictionary-submit-button"]').click({ force: true });
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if the dictionary name already exists', () => {
    cy.get('[data-testid="dictionary-create-button"]').click();
    cy.get('[data-testid="dictionary-name-input"]').type('System test orders 2');
    cy.get('[data-testid="dictionary-description-input"]').type('Dictionary description');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if file size is greater than 1 MB', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-file-button"]').click();
    });
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/too_large_file.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if dictionary file is bad formatted', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-file-button"]').click();
    });
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/invalid_orders.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if the file is not a json', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-file-button"]').click();
    });
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.txt', { force: true });

    cy.get('.p-message-error').should('exist');
    cy.get('[data-testid="dictionary-submit-button"]').should('be.disabled');
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
