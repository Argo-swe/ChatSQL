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
    cy.session('login', () => {
      cy.visit('/');
      cy.login();
    }).then(() => {
      cy.visit('/dictionary');
    });
  });

  // Test case
  it('verify that the admin can update dictionary name', () => {
    cy.get('[data-testid="update-metadata-button"]').last().click();
    cy.get('[data-testid="dictionary-name-input"]').clear();
    cy.get('[data-testid="dictionary-name-input"]').type('New test name');

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the admin can update dictionary description', () => {
    cy.get('[data-testid="update-metadata-button"]').last().click();
    cy.get('[data-testid="dictionary-description-input"]').clear();
    cy.get('[data-testid="dictionary-description-input"]').type('New test description');

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the admin can update dictionary file', () => {
    cy.get('[data-testid="update-file-button"]').last().click();
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/cinema.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
  });

  // Test case
  it('verify that the admin can download dictionary file', () => {
    cy.get('[data-testid="download-file-button"]').last().click();
    const filename = 'cypress/downloads/new_test_name.json';
    cy.readFile(filename, { timeout: 15000 }).should('exist');
  });
});
