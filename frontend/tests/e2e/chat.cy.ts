describe('Chat - HomePage', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('verify that the user can log in', () => {
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="input-username"]').type('admin');
    cy.get('[data-testid="input-password"]').type('admin');
    cy.get('[data-testid="login-submit-button"]').click();
    /* cy.window().then((win) => {
      // Accedi alla classe statica AuthService e chiama il metodo isLogged
      const isLogged = AuthService.isLogged(); 
      expect(isLogged).to.equal(true);  // Verifica che il metodo restituisca true
    }); */
  });

  it('should', () => {});
});
