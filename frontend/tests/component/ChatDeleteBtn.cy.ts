import Button from 'primevue/button';
import { createI18n } from 'vue-i18n';
import ChatDeleteBtn from '../../src/components/ChatDeleteBtn.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

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

describe('ChatDeleteBtn Component', () => {
  it('should be disabled when there are no messages', () => {
    mountChatDeleteBtn({
      messages: [],
      loading: false
    });
    cy.get('[data-testid="clean-chat-button"]').should('be.disabled');
  });

  it('should be disabled when loading is true', () => {
    mountChatDeleteBtn({
      messages: [{ message: 'Chat Message', isSent: false }],
      loading: true
    });
    cy.get('[data-testid="clean-chat-button"]').should('be.disabled');
  });

  it('should emit clear event on click', () => {
    mountChatDeleteBtn({
      messages: [{ message: 'Chat Message', isSent: false }],
      loading: false,
      onClearMessages: cy.spy().as('clearMessagesSpy')
    });
    cy.get('[data-testid="clean-chat-button"]').should('exist').click();
    cy.get('@clearMessagesSpy').should('have.been.called');
  });
});
