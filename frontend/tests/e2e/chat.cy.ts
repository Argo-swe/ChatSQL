/**
 * Test suite for prompt generation requirements.
 */
describe('Chat - HomePage', () => {
  // Hook that runs once before all tests
  before(() => {
    cy.visit('/');
    cy.setupDictionary();
  });

  // Hook that runs once after all tests
  after(() => {
    cy.login().then(() => {
      cy.cleanupDictionary();
    });
  });

  // Hook that runs before each test
  beforeEach(() => {
    cy.visit('/');
  });

  // Test case
  it('verify that a user can enter a message in the request form', () => {
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-input"]').should('have.value', 'all users');
  });

  // Test case
  it('verify that a user can select a dictionary', () => {
    cy.selectDictionary();
    cy.get('[data-testid="selected-dictionary-name"]').should(
      'have.text',
      'System Test Orders (.json)'
    );
  });

  // Test case
  it('verify that a user can preview the chosen data dictionary', () => {
    cy.selectDictionary();
    cy.get('[data-testid="dictionary-preview-button"]').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('be.visible');
    cy.get('[data-testid="database-name"]').should('have.text', 'Orders');
    cy.get('[data-testid="database-description"]').should(
      'have.text',
      'The orders database is designed to monitor and manage purchase transactions.'
    );
    cy.get('[data-testid="database-tables"] li:first').should(
      'have.text',
      'users: Table containing account details and personal information about users who make purchases.'
    );
  });

  // Test case
  it('verify that a user can send a request to get a prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').should('be.enabled').click();
    cy.get('[data-testid="chat-message-container"]').should('be.visible');
  });

  // Test case
  it('verify that the system returns an error if prompt generation fails', () => {
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').click({ force: true });
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the system returns a warning if the request is not eligible', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('123{enter}');
    let message = 'Sorry, the ChatBOT was unable to find any relevant results for "123".\n';
    message = message + 'We invite you to try again with a different request.';
    cy.get('[data-testid="request-button"]', { timeout: 15000 }).should(
      'not.have.class',
      'pi-spin pi-spinner'
    );
    cy.get('[data-testid="chat-message-container"].received', { timeout: 15000 }).should(
      'contain.text',
      message
    );
  });

  // Test case
  it('verify that the user can receive a prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users{enter}');
    cy.get('[data-testid="chat-message-container"]').should('be.visible');
    cy.get('[data-testid="request-button"]', { timeout: 15000 }).should(
      'not.have.class',
      'pi-spin pi-spinner'
    );
    cy.get('[data-testid="chat-message-container"].received', { timeout: 15000 }).should(
      'contain.text',
      'Suggested prompt'
    );
  });

  // Test case
  it('verify that the user can copy the prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users{enter}');
    cy.get('[data-testid="copy-button"]').click();
    cy.window()
      .then((win) => {
        return win.navigator.clipboard.readText();
      })
      .then((copyText) => {
        cy.get('[data-testid="chat-message-container"].received').should('contain.text', copyText);
      });
  });

  // Test case
  it('verify that the user can clear the chat history', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users{enter}');
    cy.get('[data-testid="chat-message-container"]').should('exist');
    cy.get('[data-testid="clean-chat-button"]').click();
    cy.get('[data-testid="chat-message-container"]').should('not.exist');
  });

  // Test case
  it('verify that the system supports requests in languages other than English', () => {
    cy.selectDictionary();
    cy.get('[data-testid="language-dropdown"]').click();
    cy.get('ul > li').contains('italiano').should('exist').click();
    cy.get('[data-testid="request-input"]').type('tutti gli utenti{enter}');
    cy.get('[data-testid="chat-message-container"].received', { timeout: 15000 }).should(
      'contain.text',
      'Suggested prompt'
    );
  });
});
