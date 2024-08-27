describe('Chat - HomePage', () => {
  before(() => {
    cy.visit('/');
    cy.setupDictionary();
  });

  after(() => {
    cy.visit('/');
    cy.login().then(() => {
      cy.cleanupDictionary();
    });
  });

  beforeEach(() => {
    cy.visit('/');
  });

  it('verify that a user can enter a message in the request form', () => {
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-input"]').should('have.value', 'all users');
  });

  it('verify that a user can select a dictionary', () => {
    cy.selectDictionary();
    cy.get('[data-testid="selected-dictionary-name"]').should('have.text', 'Test Orders (.json)');
  });

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

  it('verify that a user can send a request to get a prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').should('be.enabled').click();
    cy.get('[data-testid="chat-message-container"]').should('be.visible');
  });

  it('verify that the system returns an error if prompt generation fails', () => {
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').click({ force: true });
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  it('verify that the system returns a warning if the request is not eligible', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('ciao');
    cy.get('[data-testid="request-button"]').click();
    let message = 'Sorry, the ChatBOT was unable to find any relevant results for "ciao".\n';
    message = message + 'We invite you to try again with a different request.';
    cy.get('[data-testid="request-button"]', { timeout: 6000 }).should(
      'not.have.class',
      'pi-spin pi-spinner'
    );
    cy.get('[data-testid="chat-message-container"].received').should('contain.text', message);
  });

  it('verify that the user can receive a prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').click();
    cy.get('[data-testid="chat-message-container"]').should('be.visible');
    cy.get('[data-testid="request-button"]', { timeout: 6000 }).should(
      'not.have.class',
      'pi-spin pi-spinner'
    );
    cy.get('[data-testid="chat-message-container"].received').should(
      'contain.text',
      'Suggested prompt'
    );
  });

  it('verify that the user can copy the prompt', () => {
    cy.selectDictionary();
    cy.get('[data-testid="request-input"]').type('all users');
    cy.get('[data-testid="request-button"]').click();
    cy.get('[data-testid="chat-message-container"].received').invoke('text').as('prompt');
    cy.get('[data-testid="copy-button"]').click();
    cy.window()
      .then((win) => {
        // Usa la clipboard API per leggere il contenuto
        return win.navigator.clipboard.readText();
      })
      .then((clipText) => {
        cy.get('@prompt').then((text) => {
          expect(text).to.contain(clipText);
        });
      });
  });
});
