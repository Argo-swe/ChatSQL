import { createRouter, createWebHistory } from 'vue-router';
import AppMenuItem from '../../../src/components/layout/AppMenuItem.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

function mountAppMenuItem(props) {
  return cy.mount(AppMenuItem, {
    global: {
      plugins: [router]
    },
    props
  });
}

function mountItem(props?) {
  mountAppMenuItem({
    item: {
      label: 'Test',
      icon: 'pi pi-check',
      to: '/test'
    },
    ...props
  });
}

function mountItemWithSubMenu(props?) {
  mountAppMenuItem({
    item: {
      label: 'Test',
      icon: 'pi pi-check',
      to: '/test',
      items: [
        {
          label: 'Test1',
          icon: 'pi pi-check-circle',
          to: '/test1'
        },
        {
          label: 'Test2',
          icon: 'pi pi-check-square',
          to: '/test2'
        }
      ]
    },
    ...props
  });
}

describe('AppMenuItem Component', () => {
  beforeEach(() => {
    mountItem({
      root: false
    });
  });

  it('should render correctly', () => {
    cy.get('li[data-testid="menu-item"]').should('exist');
  });

  it('should display the menu item text', () => {
    cy.get('[data-testid="menu-item-text"]').should('have.text', 'Test');
  });

  it('should not be active if not clicked', () => {
    cy.get('[data-testid="menu-item"]').should('not.have.class', 'active-menuitem');
  });

  it('should be active when clicked', () => {
    cy.get('[data-testid="menu-item-link"]').should('exist').click();
    cy.get('[data-testid="menu-item"]').should('have.class', 'active-menuitem');
  });

  it('should display a root item', () => {
    mountItem({
      root: true
    });
    cy.get('[data-testid="menu-item"]').should('have.class', 'layout-root-menuitem');
    cy.get('[data-testid="menu-item-root-text"]').should('have.text', 'Test');
    cy.get('[data-testid="menu-item-text"]').should('have.text', 'Test');
  });

  it('should display an item with a submenu', () => {
    mountItemWithSubMenu({
      root: false
    });
    cy.get('[data-testid="menu-item"]')
      .find('[data-testid="menu-item-text"]')
      .first()
      .should('have.text', 'Test');
    cy.get('[data-testid="nav-submenu"]').should('be.visible');
    cy.get('[data-testid="nav-submenu"]').children().should('have.length.greaterThan', 1);
    cy.get('[data-testid="nav-submenu"]').children().first().should('have.text', 'Test1');
    cy.get('[data-testid="nav-submenu"]').children().eq(1).should('have.text', 'Test2');
  });
});
