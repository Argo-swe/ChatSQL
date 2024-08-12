import App from '../../src/App.vue';

describe('<App />', () => {
  it('renders', () => {
    cy.mount(App);
  });
});
