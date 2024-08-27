// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import Dropdown from 'primevue/dropdown';
import InputSwitch from 'primevue/inputswitch';
import Sidebar from 'primevue/sidebar';
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import { useLayout } from '@/composables/layout';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

const { layoutConfig } = useLayout();
let originalScaleValue: number;

/**
 * Performs the mounting of the ConfigSidebar component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountConfigSidebar(props?) {
  return cy.mount(ConfigSidebar, {
    global: {
      plugins: [i18n, PrimeVue],
      mocks: {
        t: (key) => key,
        layoutState: {
          configSidebarVisible: ref(true)
        }
      },
      components: {
        PgSidebar: Sidebar,
        PgButton: Button,
        PgInputSwitch: InputSwitch,
        PgDropdown: Dropdown
      }
    },
    props
  });
}

/**
 * Test suite for the ConfigSidebar component.
 */
describe('ConfigSidebar Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    originalScaleValue = layoutConfig.scale.value;
    mountConfigSidebar();
  });

  // Hook that runs after each test
  afterEach(() => {
    layoutConfig.scale.value = originalScaleValue;
  });

  // Single and isolated test case
  it('should display correctly', () => {
    cy.get('[data-testid="config-sidebar"]').should('be.visible');
    cy.get('[data-testid="manage-scale-section"]').should('be.visible');
    cy.get('[data-testid="manage-theme-section"]').should('be.visible');
    cy.get('[data-testid="manage-language-section"]').should('be.visible');
  });

  // Single and isolated test case
  it('should decrease scale', () => {
    cy.window().then((win) => {
      const originalFontSize = parseFloat(
        win.getComputedStyle(win.document.documentElement).fontSize
      );
      cy.get('[data-testid="decrease-scale-button"]').should('exist').click();
      cy.window().then(() => {
        const newFontSize = parseFloat(win.getComputedStyle(win.document.documentElement).fontSize);
        expect(newFontSize).to.be.lessThan(originalFontSize);
      });
    });
  });

  // Single and isolated test case
  it('should increase scale', () => {
    cy.window().then((win) => {
      const originalFontSize = parseFloat(
        win.getComputedStyle(win.document.documentElement).fontSize
      );
      cy.get('[data-testid="increase-scale-button"]').should('exist').click();
      cy.window().then(() => {
        const newFontSize = parseFloat(win.getComputedStyle(win.document.documentElement).fontSize);
        expect(newFontSize).to.be.greaterThan(originalFontSize);
      });
    });
  });

  // Single and isolated test case
  it('should disable decrease button', () => {
    layoutConfig.scale.value = 12;
    cy.get('[data-testid="decrease-scale-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should disable increase button', () => {
    layoutConfig.scale.value = 16;
    cy.get('[data-testid="increase-scale-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should toggle dark mode', () => {
    cy.get('[data-testid=theme-input-switch]').find('input[type="checkbox"]').check();
    cy.window().then((win) => {
      expect(win.localStorage.getItem('darkTheme')).to.equal('true');
    });

    cy.get('[data-testid=theme-input-switch]').find('input[type="checkbox"]').uncheck();
    cy.wait(100);
    cy.window().then((win) => {
      expect(win.localStorage.getItem('darkTheme')).to.equal('false');
    });
  });

  // Single and isolated test case
  it('should change the language to italian', () => {
    cy.get('[data-testid="global-language-dropdown"]').should('exist').click();
    cy.contains('locale.it').click({ force: true });
    cy.window().then((win) => {
      expect(win.localStorage.getItem('language')).to.equal('it');
    });
  });
});
