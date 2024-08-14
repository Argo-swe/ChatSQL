import ChatDeleteBtn from '../../src/components/ChatDeleteBtn.vue';
import { h } from 'vue';

describe('ChatDeleteBtn Component', () => {
    beforeEach(() => {
      cy.mount(ChatDeleteBtn, {
        setup() {
            const t = (key: any) => key;
            return { t };
        },
        props: {
          messages: [{ message: 'Chat Message', isSent: false }],
          loading: false,
        },
      });
    });
  
    it('should be disabled when there are no messages', () => {
        cy.mount(ChatDeleteBtn, {
            setup() {
                const t = (key: any) => key;
                return { t };
            },
            props: {
              messages: [],
              loading: false,
            },
        })
        cy.get('Button').should('be.disabled');
    });

    it('should be disabled when loading is true', () => {
        cy.mount(ChatDeleteBtn, {
            setup() {
                const t = (key: any) => key;
                return { t };
            },
            props: {
              messages: [{ message: 'Chat Message', isSent: false }],
              loading: true,
            },
        })
        cy.get('Button').should('be.disabled');
    });

    it('should emit clear event on click', () => {
        const clearMessagesSpy = cy.spy().as('clearMessagesSpy');

        cy.mount(ChatDeleteBtn, {
            props: {
              messages: [{ message: 'Chat Message', isSent: false }],
              loading: false,
            },
            emits: {
                'clear-messages': clearMessagesSpy
            }
        });

        // Simula il click sul pulsante
        cy.get('Button').click();

        // Verifica che l'evento sia stato emesso
        cy.get('@clearMessagesSpy').should('have.been.called');
    });
  });