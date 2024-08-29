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

    cy.get('[data-testid="dictionary-name-input"]').invoke('removeAttr', 'invalid');
    cy.get('[data-testid="dictionary-submit-button"]').invoke('removeAttr', 'disabled');
    cy.get('[data-testid="dictionary-submit-button"]').click({ force: true });
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if the dictionary name already exists', () => {
    cy.get('[data-testid="dictionary-create-button"]').click();
    cy.get('[data-testid="dictionary-name-input"]').type('System Test Orders 2');
    cy.get('[data-testid="dictionary-description-input"]').type('Dictionary description');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns an error if the dictionary description is bad formatted', () => {
    cy.getDictionaryRow().within(() => {
      cy.get('[data-testid="update-metadata-button"]').click();
    });
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('***');

    cy.get('[data-testid="dictionary-description-input"]').invoke('removeAttr', 'invalid');
    cy.get('[data-testid="dictionary-submit-button"]').invoke('removeAttr', 'disabled');
    cy.get('[data-testid="dictionary-submit-button"]').click({ force: true });
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
