import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import DebugMessage from '../../src/components/DebugMessage.vue';
import StringDataModal from '../../src/components/StringDataModal.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

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

describe('StringDataModal Component', () => {
  it('renders DebugMessage when stringData is set', () => {
    const mockDialogRef = ref({
      data: {
        stringData: 'Debug Message'
      }
    });

    mountStringDataModal(mockDialogRef);

    cy.get('[data-testid="debug-message"]').should('exist');
    cy.get('[data-testid="debug-message"]').should('have.text', 'Debug Message');
  });

  it('does not render DebugMessage when stringData is empty', () => {
    const mockDialogRef = ref({
      data: {
        stringData: ''
      }
    });

    mountStringDataModal(mockDialogRef);

    cy.get('[data-testid="debug-message"]').should('not.exist');
  });
});
