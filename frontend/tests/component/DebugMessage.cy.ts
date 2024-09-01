// External dependencies
import Button from 'primevue/button';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import DebugMessage from '@/components/DebugMessage.vue';
import UtilsService from '@/services/utils.service';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the DebugMessage component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountDebugMessage(props?) {
  return cy.mount(DebugMessage, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key
      },
      components: {
        PgButton: Button
      }
    },
    props
  });
}

/**
 * Test suite for the DebugMessage component.
 */
describe('DebugMessage Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    cy.spy(UtilsService, 'downloadFile').as('downloadFileSpy');

    mountDebugMessage({
      message: 'Debug Message'
    });
  });

  // Single and isolated test case
  it('should display the correct message', () => {
    cy.get('[data-testid="debug-message"]').should('have.text', 'Debug Message');
  });

  // Single and isolated test case
  it('should trigger file download with correct message', () => {
    cy.get('[data-testid="debug-message-download"]').should('exist').click();
    cy.get('@downloadFileSpy').should('have.been.calledWith', 'chatsql_log.txt', 'Debug Message');
  });
});
