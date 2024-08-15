import { createI18n } from 'vue-i18n';
import Button from 'primevue/button';
import ChatDeleteBtn from '../../src/components/ChatDeleteBtn.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: "Mock translation"
});

function mountChatDeleteBtn(props?, emits?) {
  return cy.mount(ChatDeleteBtn, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key,
      },
      components: {
        PgButton: Button
      }
    },
    props,
    emits
  });
}

describe('ChatDeleteBtn Component', () => {
  it('should be disabled when there are no messages', () => {
    mountChatDeleteBtn(
      {
        messages: [],
        loading: false
      }
    );
    cy.get('Button').should('be.disabled');
  });

  it('should be disabled when loading is true', () => {
    mountChatDeleteBtn(
      {
        messages: [{ message: 'Chat Message', isSent: false }],
        loading: true
      }
    );
    cy.get('Button').should('be.disabled');
  });
  
  it('should emit clear event on click', () => {
    const clearMessagesSpy = cy.spy().as('clearMessagesSpy');

    mountChatDeleteBtn(
      {
        messages: [{ message: 'Chat Message', isSent: false }],
        loading: false
      },
      {
        'clear-messages': clearMessagesSpy
      }
    );

    cy.get('Button')
      .should('exist')
      .click();

    cy.get('@clearMessagesSpy').should('have.been.called');
  });
});
