// External dependencies
import { ref } from 'vue';
import { createI18n } from 'vue-i18n';

// Internal dependencies
import DebugMessage from '@/components/DebugMessage.vue';
import StringDataModal from '@/components/StringDataModal.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the StringDataModal component.
 * @param mockDialogRef - A mock of the dialogRef object, containing the data passed from the parent object.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountStringDataModal(mockDialogRef, props?) {
  return cy.mount(StringDataModal, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key
      },
      provide: {
        dialogRef: mockDialogRef
      },
      components: {
        DebugMessage
      }
    },
    props
  });
}

/**
 * Test suite for the StringDataModal component.
 */
describe('StringDataModal Component', () => {
  // Single and isolated test case
  it('should render debug message when stringData is set', () => {
    const mockDialogRef = ref({
      data: {
        stringData: 'Debug Message'
      }
    });
    mountStringDataModal(mockDialogRef);

    cy.get('[data-testid="debug-message"]').should('exist');
    cy.get('[data-testid="debug-message"]').should('have.text', 'Debug Message');
  });

  // Single and isolated test case
  it('should not render debug message when stringData is empty', () => {
    const mockDialogRef = ref({
      data: {
        stringData: ''
      }
    });
    mountStringDataModal(mockDialogRef);

    cy.get('[data-testid="debug-message"]').should('not.exist');
  });
});
