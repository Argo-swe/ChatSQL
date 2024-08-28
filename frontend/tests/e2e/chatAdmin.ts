/**
 * Test suite for prompt generation with debug requirements.
 */
describe('Chat - HomePage', () => {
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
      cy.visit('/');
    });
  });

  // Test case
  it('verify that the system generates a log if the request is sent by the admin', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users{enter}');
    cy.get('[data-testid="debug-button"]', { timeout: 15000 }).should('exist').click();
    cy.get('[data-testid="debug-message"]').should('contain.text', 'Request: all users');
  });

  // Test case
  it('verify that the admin can download a log file', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users{enter}');
    cy.get('[data-testid="debug-button"]', { timeout: 15000 }).should('exist').click();
    cy.get('[data-testid="debug-message-download"]').should('exist').click();
    const filename = 'cypress/downloads/chatsql_log.txt';
    cy.readFile(filename, { timeout: 15000 }).should('contain', 'Request: all users');
  });
});
