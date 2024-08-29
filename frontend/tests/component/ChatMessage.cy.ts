// External dependencies
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import ChatMessage from '@/components/ChatMessage.vue';
import StringDataModal from '@/components/StringDataModal.vue';
import AuthService from '@/services/auth.service';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the ChatMessage component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
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

/**
 * Mounts a chat message representing a request sent by the user.
 */
function UserRequest() {
  return mountChatMessage({
    message: 'Chat Request Message',
    isSent: true
  });
}

/**
 * Mounts a chat message representing a response sent by the ChatBOT to the user.
 */
function ChatBotResponse() {
  return mountChatMessage({
    message: 'Chat Response Message',
    isSent: false
  });
}

/**
 * Mounts a chat message representing a response sent by the ChatBOT to the admin.
 */
function ChatBotResponseWithDebug() {
  return mountChatMessage({
    message: 'Chat Response Message',
    isSent: false,
    debug: 'Prompt generation debug'
  });
}

/**
 * Verify that the call heard by the spy invoked the StringDataModal component.
 */
function CheckSubComponentCall() {
  cy.get('@openDialogSpy').should('have.been.called');
  cy.get('@openDialogSpy').its('firstCall.args[0]').should('equal', StringDataModal);
}

/**
 * Test suite for the ChatMessage component.
 */
describe('ChatMessage Component', () => {
  // Single and isolated test case
  it('should display the user message correctly', () => {
    UserRequest();
    cy.get('[data-testid="chat-message-container"]').should('have.class', 'sent');
    cy.get('[data-testid="message-avatar"]').find('.pi').should('have.class', 'pi-user');
    cy.get('[data-testid="chat-message"]').should('have.text', 'Chat Request Message');
  });

  // Single and isolated test case
  it('should display the chatbot message correctly', () => {
    ChatBotResponse();
    cy.get('[data-testid="chat-message-container"]').should('have.class', 'received');
    cy.get('[data-testid="message-avatar"]').find('.pi').should('have.class', 'pi-database');
    cy.get('[data-testid="chat-message"]').should('have.text', 'Chat Response Message');
  });

  // Single and isolated test case
  it('should hide the action area if the message has been sent by a user', () => {
    UserRequest();
    cy.get('[data-testid="copy-button"]').should('not.exist');
    cy.get('[data-testid="debug-button"]').should('not.exist');
  });

  // Single and isolated test case
  it('should call the copy to clipboard function with correct data', () => {
    cy.window().then((win) => {
      cy.spy(win.navigator.clipboard, 'writeText').as('clipboardSpy');
    });
    ChatBotResponse();
    cy.get('[data-testid="copy-button"]').should('exist').click();
    cy.get('@clipboardSpy').should('be.calledWith', 'Chat Response Message');
  });

  // Single and isolated test case
  it('should hide debug button if the user is not logged in', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    ChatBotResponseWithDebug();
    cy.get('[data-testid="debug-button"]').should('not.exist');
  });

  // Single and isolated test case
  it('should display debug modal when clicking the debug button', () => {
    cy.stub(AuthService, 'isLogged').returns(true);

    ChatBotResponseWithDebug().then(({ component }) => {
      const openDialogSpy = cy.spy(component.dialog, 'open').as('openDialogSpy');

      cy.get('[data-testid="debug-button"]')
        .should('exist')
        .click()
        .then(() => {
          CheckSubComponentCall();
          const callArgs = openDialogSpy.getCall(0).args[1];
          expect(callArgs.data.stringData).to.equal('Prompt generation debug');
        });
    });
  });
});
