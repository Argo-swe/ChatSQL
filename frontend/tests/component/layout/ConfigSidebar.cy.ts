import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import Dropdown from 'primevue/dropdown';
import InputSwitch from 'primevue/inputswitch';
import Sidebar from 'primevue/sidebar';
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import ConfigSidebar from '../../../src/components/layout/ConfigSidebar.vue';
import { useLayout } from '../../../src/composables/layout';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

let originalScaleValue: number;

function mountConfigSidebar(mockLayoutConfig?, props?) {
  return cy.mount(ConfigSidebar, {
    global: {
      plugins: [i18n, PrimeVue],
      mocks: {
        t: (key) => key,
        layoutState: {
          configSidebarVisible: ref(true)
        },
        ...mockLayoutConfig
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

describe('ConfigSidebar Component', () => {
  beforeEach(() => {
    const { layoutConfig } = useLayout();
    originalScaleValue = layoutConfig.scale.value;
    mountConfigSidebar();
  });

  afterEach(() => {
    const { layoutConfig } = useLayout();
    layoutConfig.scale.value = originalScaleValue;
  });

  it('should display correctly', () => {
    cy.get('[data-testid="config-sidebar"]').should('be.visible');
    cy.get('[data-testid="manage-scale-section"]').should('be.visible');
    cy.get('[data-testid="manage-theme-section"]').should('be.visible');
    cy.get('[data-testid="manage-language-section"]').should('be.visible');
  });

  it('should decrease scale', () => {
    cy.window().then((win) => {
      const originalFontSize = parseFloat(
        win.getComputedStyle(win.document.documentElement).fontSize
      );
      cy.get('[data-testid="decrease-scale-button"]').click();
      cy.window().then(() => {
        const newFontSize = parseFloat(win.getComputedStyle(win.document.documentElement).fontSize);
        expect(newFontSize).to.be.lessThan(originalFontSize);
      });
    });
  });

  it('should increase scale', () => {
    cy.window().then((win) => {
      const originalFontSize = parseFloat(
        win.getComputedStyle(win.document.documentElement).fontSize
      );
      cy.get('[data-testid="increase-scale-button"]').click();
      cy.window().then(() => {
        const newFontSize = parseFloat(win.getComputedStyle(win.document.documentElement).fontSize);
        expect(newFontSize).to.be.greaterThan(originalFontSize);
      });
    });
  });

  it('should disable decrease button', () => {
    mountConfigSidebar({
      layoutConfig: {
        scale: ref(12),
        theme: ref('aura-light-blue'),
        darkTheme: ref(false)
      }
    });
    cy.get('[data-testid="decrease-scale-button"]').should('be.disabled');
  });

  it('should disable increase button', () => {
    mountConfigSidebar({
      layoutConfig: {
        scale: ref(16),
        theme: ref('aura-light-blue'),
        darkTheme: ref(false)
      }
    });
    cy.get('[data-testid="increase-scale-button"]').should('be.disabled');
  });

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

  it('should change the language to italian', () => {
    cy.get('[data-testid="language-dropdown"]').click();
    cy.contains('locale.it').click({ force: true });
    cy.window().then((win) => {
      expect(win.localStorage.getItem('language')).to.equal('it');
    });
  });
});
