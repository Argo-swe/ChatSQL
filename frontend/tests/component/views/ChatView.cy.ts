// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import Divider from 'primevue/divider';
import Dropdown from 'primevue/dropdown';
import InputGroup from 'primevue/inputgroup';
import Textarea from 'primevue/textarea';
import ToastService from 'primevue/toastservice';
import ToggleButton from 'primevue/togglebutton';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import ChatDeleteBtn from '../../../src/components/ChatDeleteBtn.vue';
import ChatMessage from '../../../src/components/ChatMessage.vue';
import DictPreview from '../../../src/components/DictPreview.vue';
import ApiClientManager from '../../../src/services/api-client.service';
import AuthService from '../../../src/services/auth.service';
import MessageService from '../../../src/services/message.service';
import ChatView from '../../../src/views/ChatView.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the ChatView component.
 * @param mockApiClient - The mock API client that replaces the real API client to simulate calls.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountChatView(mockApiClient: any = getGlobalMockApiClient(), props?) {
  cy.spy(MessageService.prototype, 'messageSuccess').as('messageSuccessSpy');
  cy.spy(MessageService.prototype, 'messageError').as('messageErrorSpy');
  cy.stub(ApiClientManager, 'getApiClient').returns(mockApiClient);

  return cy.mount(ChatView, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService],
      mocks: {
        t: (key) => key,
        handleEnterKeyRequest: cy.spy().as('handleEnterKeyRequestSpy')
      },
      components: {
        PgToggleButton: ToggleButton,
        PgDivider: Divider,
        PgInputGroup: InputGroup,
        PgDropdown: Dropdown,
        PgButton: Button,
        PgTextarea: Textarea,
        ChatDeleteBtn,
        DictPreview,
        ChatMessage
      }
    },
    props
  });
}

/**
 * Returns a global mock API client with stubs that simulate API calls.
 */
function getGlobalMockApiClient() {
  return {
    getAllDictionaries: cy.stub().resolves({
      data: {
        status: 'OK',
        data: [
          {
            id: 1,
            name: 'Orders',
            description: 'Orders dictionary'
          }
        ]
      }
    }),
    getDictionaryPreview: cy.stub().resolves({
      data: {
        status: 'OK',
        data: {
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
      }
    })
  };
}

/**
 * Returns a successful mock response for the generatePrompt API call.
 */
function getPromptSuccessResponse() {
  return {
    data: {
      status: 'OK',
      data: 'Chat Response Message'
    }
  };
}

/**
 * Returns a successful mock response for the generatePromptWithDebug API call.
 */
function getPromptWithDebugSuccessResponse() {
  return {
    data: {
      status: 'OK',
      data: {
        prompt: 'Chat Response Message',
        debug: 'Prompt generation debug'
      }
    }
  };
}

/**
 * Returns a mock error response for the API call.
 */
function getFailureResponse() {
  return {
    data: {
      status: 'ERROR',
      message: 'Error while generating prompt'
    }
  };
}

/**
 * Mount the ChatView component with a custom mock API client for prompt generation.
 * @param response - The mock response to return.
 */
function mockGeneratePrompt(response: any = getPromptSuccessResponse()) {
  const mockApiClient = {
    ...getGlobalMockApiClient(),
    generatePrompt: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.generatePrompt).as('generatePrompt');
  return mountChatView(mockApiClient);
}

/**
 * Mount the ChatView component with a custom mock API client for prompt with debug generation.
 * @param response - The mock response to return.
 */
function mockGeneratePromptWithDebug(response: any = getPromptWithDebugSuccessResponse()) {
  const mockApiClient = {
    ...getGlobalMockApiClient(),
    generatePromptWithDebug: cy.stub().resolves(response)
  };
  cy.wrap(mockApiClient.generatePromptWithDebug).as('generatePromptWithDebug');
  return mountChatView(mockApiClient);
}

/**
 * Simulates selecting a dictionary within a dropdown menu.
 */
function selectDictionary() {
  cy.get('[data-testid="dictionary-dropdown"]').click();
  cy.get('ul > li').contains('Orders').should('exist').click();
}

/**
 * Test suite for the ChatView component.
 */
describe('ChatView Component', () => {
  // Single and isolated test case
  it('should render the chat correctly', () => {
    mountChatView();
    cy.get('[data-testid="chat"]').should('be.visible');
    cy.get('[data-testid="title-bar-container"]').should('be.visible');
    cy.get('[data-testid="request-container"]').should('be.visible');
  });

  // Single and isolated test case
  it('should hide select view when clicking the toggle button', () => {
    mountChatView();
    cy.get('[data-testid="select-view"]').should('be.visible');
    cy.get('[data-testid="title-bar-toggle-button"]').find('.pi').should('have.class', 'pi-times');
    cy.get('[data-testid="title-bar-toggle-button"]').find('input[type="checkbox"]').check();
    cy.get('[data-testid="select-view"]').should('not.be.visible');
    cy.get('[data-testid="title-bar-toggle-button"]').find('.pi').should('have.class', 'pi-check');
  });

  // Single and isolated test case
  it('should handle dictionary selection', () => {
    mountChatView();
    selectDictionary();
    cy.get('[data-testid="selected-dictionary-name"]').should('have.text', 'Orders (.json)');
    cy.window().then((win) => {
      expect(win.localStorage.getItem('chat-dictionary-id')).to.equal('1');
    });
  });

  // Single and isolated test case
  it('should display dictionary preview', () => {
    mountChatView();
    cy.get('[data-testid="dictionary-preview-button"]').should('be.disabled');
    selectDictionary();
    cy.get('[data-testid="dictionary-preview-button"]').should('be.enabled').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('be.visible');
  });

  // Single and isolated test case
  it('should toggle dictionary preview and chat messages', () => {
    mockGeneratePrompt();
    selectDictionary();
    /**
     * Opens the dictionary preview.
     */
    cy.get('[data-testid="dictionary-preview-button"]').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('exist');
    /**
     * Sends a request that overlaps the dictionary preview.
     */
    cy.get('[data-testid="request-input"]').type('all orders');
    cy.get('[data-testid="request-button"]').click();
    cy.get('[data-testid="chat-message-container"]').should('exist');
    cy.get('[data-testid="dictionary-preview-container"]').should('not.exist');
    /**
     * Reopens the preview of the dictionary and hides the chat messages.
     */
    cy.get('[data-testid="dictionary-preview-button"]').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('exist');
    cy.get('[data-testid="chat-message-container"]').should('not.exist');
    /**
     * Closes the preview and shows the messages again.
     */
    cy.get('[data-testid="dictionary-preview-hide-button"]').click();
    cy.get('[data-testid="dictionary-preview-container"]').should('not.exist');
    cy.get('[data-testid="chat-message-container"]').should('exist');
  });

  // Single and isolated test case
  it('should disable the submit button if dictionary is not selected', () => {
    mountChatView();
    cy.get('[data-testid="request-input"]').type('all orders');
    cy.get('[data-testid="request-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should disable the submit button if request is not typed', () => {
    mountChatView();
    selectDictionary();
    cy.get('[data-testid="request-button"]').should('be.disabled');
  });

  // Single and isolated test case
  it('should send the request when enter key is pressed', () => {
    mockGeneratePrompt();
    selectDictionary();
    cy.get('[data-testid="request-input"]').type('all orders{enter}');
    cy.get('@handleEnterKeyRequestSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle prompt generation successfully', () => {
    mockGeneratePrompt();
    selectDictionary();
    cy.get('[data-testid="dbms-dropdown"]').click();
    cy.get('ul > li').contains('PostgreSQL').should('exist').click();
    cy.get('[data-testid="language-dropdown"]').click();
    cy.get('ul > li').contains('spanish').should('exist').click();
    cy.get('[data-testid="request-input"]').type('all orders');
    cy.get('[data-testid="request-button"]').should('be.enabled').click();
    cy.get('@generatePrompt').should('have.been.calledWith', {
      dictionaryId: 1,
      query: 'all orders',
      dbms: 'PostgreSQL',
      lang: 'spanish'
    });
    cy.get('[data-testid="chat-message-container"]').should('exist');
    cy.window().then((win) => {
      const messages = JSON.parse(win.sessionStorage.getItem('chat-messages'));
      expect(messages[1].message).to.equal('Chat Response Message');
    });
    cy.get('[data-testid="request-input"]').should('be.empty');
  });

  // Single and isolated test case
  it('should handle prompt generation failure', () => {
    mockGeneratePrompt(getFailureResponse());
    selectDictionary();
    cy.get('[data-testid="request-input"]').type('invalid request');
    cy.get('[data-testid="request-button"]').click();
    cy.get('@messageErrorSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should handle prompt with debug generation successfully', () => {
    cy.stub(AuthService, 'isLogged').returns(true);
    mockGeneratePromptWithDebug();
    selectDictionary();
    cy.get('[data-testid="request-input"]').type('all orders');
    cy.get('[data-testid="request-button"]').click();
    cy.get('[data-testid="chat-message-container"]').should('exist');
    cy.get('[data-testid="debug-button"]').should('exist');
  });

  // Single and isolated test case
  it('should clear the chat history when clicking delete button', () => {
    mockGeneratePrompt();
    selectDictionary();
    cy.get('[data-testid="request-input"]').type('all orders');
    cy.get('[data-testid="request-button"]').click();
    cy.get('[data-testid="chat-message-container"]').should('exist');
    cy.get('[data-testid="clean-chat-button"]').should('exist').click();
    cy.get('[data-testid="chat-message-container"]').should('not.exist');
  });
});
