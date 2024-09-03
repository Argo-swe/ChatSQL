// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

import '@cypress/code-coverage/support';

declare global {
  namespace Cypress {
    interface Chainable {
      setupDictionary(): Chainable<void>;
      cleanupDictionary(): Chainable<void>;
      login(): Chainable<void>;
      logout(): Chainable<void>;
      handleSession(): Chainable<void>;
      selectDictionary(): Chainable<void>;
      getDictionaryRow(): Chainable<void>;
      decreaseScale(): Chainable<void>;
      increaseScale(): Chainable<void>;
    }
  }
}

/**
 * Cypress command to login.
 */
Cypress.Commands.add('login', () => {
  cy.get('[data-testid="login-button"]').click();
  cy.get('[data-testid="input-username"]').type('admin');
  cy.get('[data-testid="input-password"]').type('admin');
  cy.get('[data-testid="login-submit-button"]').click();
});

/**
 * Cypress command to logout.
 */
Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="logout-button"]').click({ force: true });
  cy.get('[data-testid="confirm-dialog"]')
    .find('[data-pc-name="acceptbutton"]')
    .click({ force: true });
});

/**
 * Cypress command to handle access via session management.
 */
Cypress.Commands.add('handleSession', () => {
  cy.session('login', () => {
    cy.visit('/');
    cy.login();
  });
});

/**
 * Cypress command to insert a dictionary to use as a basis for tests.
 */
Cypress.Commands.add('setupDictionary', () => {
  cy.visit('/dictionary');
  cy.get('[data-testid="dictionary-create-button"]').click();
  cy.get('[data-testid="dictionary-name-input"]').type('System test orders');
  cy.get('[data-testid="dictionary-description-input"]').type('System test orders dictionary');
  cy.get('[data-testid="dictionary-file-upload"]')
    .find('input[type="file"]')
    .selectFile('cypress/fixtures/orders.json', { force: true });

  cy.get('[data-testid="dictionary-submit-button"]').click();
  cy.get('[data-testid="toast-message"]', { timeout: 120000 }).should('be.visible');
});

/**
 * Cypress command to retrieve a specific dictionary row by searching the table.
 */
Cypress.Commands.add('getDictionaryRow', () => {
  cy.get('[data-testid="dictionaries-table"] tr').contains('System test orders').parents('tr');
});

/**
 * Cypress command to delete the dictionary at the end of tests.
 */
Cypress.Commands.add('cleanupDictionary', () => {
  cy.visit('/dictionary');
  cy.getDictionaryRow().within(() => {
    cy.get('[data-testid="dictionary-delete-button"]').click();
  });
  cy.get('[data-testid="confirm-dialog"]').find('[data-pc-name="acceptbutton"]').click();
  cy.get('[data-testid="toast-message"]').find('.p-toast-message-success').should('exist');
});

/**
 * Cypress command to select a data dictionary.
 */
Cypress.Commands.add('selectDictionary', () => {
  cy.get('[data-testid="dictionary-dropdown"]').click();
  cy.get('ul > li').contains('System test orders').click();
});
