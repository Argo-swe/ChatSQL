import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';
import ChatMessage from '../../src/components/ChatMessage.vue';
import StringDataModal from '../../src/components/StringDataModal.vue';
import AuthService from '../../src/services/auth.service';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountChatMessage(props?) {
  return cy.mount(ChatMessage, {
    global: {
      plugins: [i18n, DialogService, ToastService],
      mocks: {
        t: (key) => key
      },
      components: {
        PgAvatar: Avatar,
        PgButton: Button,
        StringDataModal
      }
    },
    props
  });
}

function UserRequest() {
  return mountChatMessage({
    message: 'Chat Request Message',
    isSent: true
  });
}

function ChatBotResponse() {
  return mountChatMessage({
    message: 'Chat Response Message',
    isSent: false
  });
}

function ChatBotResponseWithDebug() {
  return mountChatMessage({
    message: 'Chat Response Message',
    isSent: false,
    debug: 'Prompt generation debug'
  });
}

describe('ChatMessage Component', () => {
  it('should display the user message with correct classes', () => {
    UserRequest();
    cy.get('[data-testid="chat-message-container"]').should('have.class', 'sent');
    cy.get('[data-testid="message-avatar"]').find('.pi').should('have.class', 'pi-user');
    cy.get('[data-testid="chat-message"]').should('contain.text', 'Chat Request Message');
  });

  it('should display the chatbot message with correct classes', () => {
    ChatBotResponse();
    cy.get('[data-testid="chat-message-container"]').should('have.class', 'received');
    cy.get('[data-testid="message-avatar"]').find('.pi').should('have.class', 'pi-database');
    cy.get('[data-testid="chat-message"]').should('contain.text', 'Chat Response Message');
  });

  it('should hide the buttons if the message has been sent by a user', () => {
    UserRequest();
    cy.get('[data-testid="copy-button"]').should('not.exist');
    cy.get('[data-testid="debug-button"]').should('not.exist');
  });

  it('should call the copy to clipboard function with correct data', () => {
    // Intercepts the call to 'navigator.clipboard.writeText' and simulate a success
    cy.window().then((win) => {
      const clipboardStub = cy.stub(win.navigator.clipboard, 'writeText').resolves();
      cy.wrap(clipboardStub).as('clipboardStub');
    });
    ChatBotResponse();
    cy.get('[data-testid="copy-button"]').should('exist').click();
    cy.get('@clipboardStub').should('be.calledWith', 'Chat Response Message');
  });

  it('should hide debug button if the user is not logged in', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    ChatBotResponseWithDebug();
    cy.get('[data-testid="debug-button"]').should('not.exist');
  });

  it('shows debug modal when clicking the debug button', () => {
    cy.stub(AuthService, 'isLogged').returns(true);

    ChatBotResponseWithDebug().then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="debug-button"]')
        .click()
        .then(() => {
          expect(openDialogSpy).to.be.called;

          let callArgs = openDialogSpy.getCall(0).args[0];
          expect(callArgs).to.equal(StringDataModal);
          callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.stringData).to.equal('Prompt generation debug');
        });
    });
  });
});
