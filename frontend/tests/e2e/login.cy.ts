/**
 * Performs the login process for an admin user.
 */
function Login() {
  cy.get('[data-testid="login-button"]').click();
  cy.get('[data-testid="input-username"]').type('admin');
  cy.get('[data-testid="input-password"]').type('admin');
  cy.get('[data-testid="login-submit-button"]').click();
}

/**
 * Test suite for login and logout requirements.
 */
describe('Chat - HomePage', () => {
  // Hook that runs before each tests
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-testid="open-settings-button"]').click();
    cy.get('[data-testid="global-language-dropdown"]').click();
    cy.get('li')
      .find('[data-testid="global-language-option"]')
      .contains('inglese')
      .click({ force: true });
    cy.get('body').click(0, 0);
  });

  // Test case
  it('verify that the user can log in', () => {
    Login();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-success').should('exist');
    cy.get('[data-testid="logout-button"]').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length', 2);
  });

  // Test case
  it('verify that login fails with incorrect credentials', () => {
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="input-username"]').type('admin');
    cy.get('[data-testid="input-password"]').type('password123');
    cy.get('[data-testid="login-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that login fails for an unregistered user', () => {
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="input-username"]').type('user');
    cy.get('[data-testid="input-password"]').type('password123');
    cy.get('[data-testid="login-submit-button"]').click();
    cy.get('[data-testid="toast-message"]').find('.p-toast-message-error').should('exist');
  });

  // Test case
  it('verify that the admin can log out', () => {
    Login();
    cy.get('[data-testid="logout-button"]').click();
    cy.get('[data-testid="confirm-dialog"]').find('[data-pc-name="acceptbutton"]').click();
    cy.get('[data-testid="login-button"]').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length', 1);
  });
});
