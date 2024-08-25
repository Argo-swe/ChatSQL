// External dependencies
import Button from 'primevue/button';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import ChatDeleteBtn from '@/components/ChatDeleteBtn.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the ChatDeleteBtn component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountChatDeleteBtn(props?) {
  return cy.mount(ChatDeleteBtn, {
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
 * Test suite for the ChatDeleteBtn component.
 */
describe('ChatDeleteBtn Component', () => {
  // Single and isolated test case
  it('should be disabled when there are no messages', () => {
    mountChatDeleteBtn({
      messages: [],
      loading: false
    });
    cy.get('[data-testid="clean-chat-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should be disabled when loading is true', () => {
    mountChatDeleteBtn({
      messages: [{ message: 'Chat Message', isSent: false }],
      loading: true
    });
    cy.get('[data-testid="clean-chat-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should emit clear event on click', () => {
    mountChatDeleteBtn({
      messages: [{ message: 'Chat Message', isSent: false }],
      loading: false,
      onClearMessages: cy.spy().as('clearMessagesSpy')
    });
    cy.get('[data-testid="clean-chat-button"]').should('be.enabled').click();
    cy.get('@clearMessagesSpy').should('have.been.called');
  });
});
