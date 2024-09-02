// Internal dependencies
import App from '@/App.vue';

/**
 * Test suite for the App component.
 */
describe('App Component', () => {
  // Single and isolated test case
  it('should render correctly', () => {
    cy.mount(App);
  });
});
