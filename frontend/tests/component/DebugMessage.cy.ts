import Button from 'primevue/button';
import { createI18n } from 'vue-i18n';
import DebugMessage from '../../src/components/DebugMessage.vue';
import UtilsService from '../../src/services/utils.service';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountDebugMessage(props?, emits?) {
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
    props,
    emits
  });
}

describe('DebugMessage Component', () => {
  it('should display the correct message', () => {
    mountDebugMessage({
      message: 'Debug Message'
    });
    cy.get('[data-testid="debug-message"]').should('contain.text', 'Debug Message');
  });

  it('should trigger file download with correct message', () => {
    cy.spy(UtilsService, 'downloadFile').as('downloadFileSpy');

    mountDebugMessage({
      message: 'Debug Message'
    });
    cy.get('Button[data-testid="debug-message-download"]').click();

    cy.get('@downloadFileSpy').should('have.been.calledWith', 'chatsql_log.txt', 'Debug Message');
  });
});
