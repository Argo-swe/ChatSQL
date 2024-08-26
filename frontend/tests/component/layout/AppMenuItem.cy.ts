// External dependencies
import { createRouter, createWebHistory } from 'vue-router';

// Internal dependencies
import AppMenuItem from '@/components/layout/AppMenuItem.vue';

// Mock VueRouter
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

/**
 * Performs the mounting of the AppMenuItem component.
 * @param props - Properties to pass to the component during mount.
 */
function mountAppMenuItem(props) {
  return cy.mount(AppMenuItem, {
    global: {
      plugins: [router]
    },
    props
  });
}

/**
 * Mounts a simple menu item.
 * @param props - (Optional) Additional properties to pass to the component during mount.
 */
function mountItem(props?) {
  return mountAppMenuItem({
    item: {
      label: 'Test',
      icon: 'pi pi-check',
      to: '/test'
    },
    ...props
  });
}

/**
 * Mounts a menu item with submenu.
 * @param props - (Optional) Additional properties to pass to the component during mount.
 */
function mountItemWithSubMenu(props?) {
  return mountAppMenuItem({
    item: {
      label: 'Test',
      icon: 'pi pi-check',
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

/**
 * Test suite for the AppMenuItem component.
 */
describe('AppMenuItem Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    mountItem({
      root: false
    });
  });

  // Single and isolated test case
  it('should render correctly', () => {
    cy.get('[data-testid="menu-item"]').should('exist');
  });

  // Single and isolated test case
  it('should display the text of the menu item', () => {
    cy.get('[data-testid="menu-item-text"]').should('have.text', 'Test');
  });

  // Single and isolated test case
  it('should not be active if not clicked', () => {
    cy.get('[data-testid="menu-item"]').should('not.have.class', 'active-menuitem');
  });

  // Single and isolated test case
  it('should be active when clicked', () => {
    cy.get('[data-testid="menu-item-link"]').should('exist').click();
    cy.get('[data-testid="menu-item"]').should('have.class', 'active-menuitem');
  });

  // Single and isolated test case
  it('should display a root item', () => {
    mountItem({
      root: true
    });
    cy.get('[data-testid="menu-item"]').should('have.class', 'layout-root-menuitem');
    cy.get('[data-testid="menu-item-root-text"]').should('have.text', 'Test');
    cy.get('[data-testid="menu-item-text"]').should('have.text', 'Test');
  });

  // Single and isolated test case
  it('should handle an item with a submenu', () => {
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
    cy.get('[data-testid="menu-item"]').find('[data-testid="menu-item-link"]').first().click();
    cy.get('[data-testid="nav-submenu"]').should('not.be.visible');
  });
});
