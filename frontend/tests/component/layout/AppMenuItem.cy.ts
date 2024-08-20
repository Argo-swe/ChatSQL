import { createRouter, createWebHistory } from 'vue-router';
import AppMenuItem from '../../../src/components/layout/AppMenuItem.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

function mountAppMenuItem(props?) {
  return cy.mount(AppMenuItem, {
    global: {
      plugins: [router]
    },
    props: {
      item: {
        label: 'Test',
        icon: 'pi pi-check',
        to: '/test'
      }
    }
  });
}

describe('AppMenuItem', () => {
  it('should render correctly', () => {
    mountAppMenuItem();

    cy.get('li[data-testid="menu-item"]').should('exist');
  });

  it('should display the menu item text', () => {
    mountAppMenuItem();

    cy.get('[data-testid="menu-item"] .layout-menuitem-text').should('contain.text', 'Test');
  });

  it('should not be active if not clicked', () => {
    mountAppMenuItem();

    cy.get('[data-testid="menu-item"]').should('not.have.class', 'active-menuitem');
  });

  it('should be active when clicked', () => {
    mountAppMenuItem();

    cy.get('[data-testid="menu-item"] a').click();
    cy.get('[data-testid="menu-item"]').should('have.class', 'active-menuitem');
  });
});