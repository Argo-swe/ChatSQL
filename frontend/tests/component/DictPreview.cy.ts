// External dependencies
import Button from 'primevue/button';
import ScrollPanel from 'primevue/scrollpanel';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import DictPreview from '@/components/DictPreview.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the DictPreview component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountDictPreview(props?) {
  return cy.mount(DictPreview, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key
      },
      components: {
        PgScrollPanel: ScrollPanel,
        PgButton: Button
      }
    },
    props
  });
}

/**
 * Test suite for the DictPreview component.
 */
describe('DictPreview Component', () => {
  // Single and isolated test case
  it('should not render if detailsVisible equals false', () => {
    mountDictPreview({
      detailsVisible: false,
      dictionaryPreview: {
        databaseName: '',
        databaseDescription: '',
        tables: []
      }
    });
    cy.get('[data-testid="dictionary-preview-container"]').should('not.exist');
  });

  // Single and isolated test case
  it('should render with correct data', () => {
    mountDictPreview({
      detailsVisible: true,
      dictionaryPreview: {
        databaseName: 'Orders',
        databaseDescription: 'Orders database',
        tables: [
          {
            name: 'Products',
            description: 'Products table'
          },
          {
            name: 'Users',
            description: 'Users table'
          }
        ]
      }
    });
    cy.get('[data-testid="dictionary-preview-container"]').should('exist');
    cy.get('[data-testid="database-name"]').should('have.text', 'Orders');
    cy.get('[data-testid="database-description"]').should('have.text', 'Orders database');
    cy.get('[data-testid="database-tables"] li:first').should(
      'have.text',
      'Products: Products table'
    );
    cy.get('[data-testid="database-tables"] li:nth-child(2)').should(
      'have.text',
      'Users: Users table'
    );
  });

  // Single and isolated test case
  it('should toggle expansion state on click', () => {
    mountDictPreview({
      detailsVisible: true,
      dictionaryPreview: {
        databaseName: '',
        databaseDescription: '',
        tables: []
      }
    });
    cy.get('[data-testid="dictionary-preview-expand-button"]').should('exist').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('have.class', 'expanded');
    cy.get('[data-testid="dictionary-preview-expand-button"]')
      .find('.pi')
      .should('have.class', 'pi-window-minimize');

    cy.get('[data-testid="dictionary-preview-expand-button"]').click({ force: true });
    cy.get('[data-testid="dictionary-preview-container"]').should('not.have.class', 'expanded');
    cy.get('[data-testid="dictionary-preview-expand-button"]')
      .find('.pi')
      .should('have.class', 'pi-expand');
  });

  // Single and isolated test case
  it('should emit hide details event on click', () => {
    mountDictPreview({
      detailsVisible: true,
      dictionaryPreview: {
        databaseName: '',
        databaseDescription: '',
        tables: []
      },
      onHideDetails: cy.spy().as('hideDetailsSpy')
    });
    cy.get('[data-testid="dictionary-preview-hide-button"]').should('exist').click();
    cy.get('@hideDetailsSpy').should('have.been.called');
  });
});
