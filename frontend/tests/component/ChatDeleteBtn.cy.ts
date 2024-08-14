import Button from 'primevue/button';
import ChatDeleteBtn from '../../src/components/ChatDeleteBtn.vue';

function mountChatDeleteBtn(props, emits) {
  return cy.mount(ChatDeleteBtn, {
    global: {
      components: {
        PgButton: Button
      }
    },
    setup() {
      const t = (key) => key; // Mock the t function
      return { t };
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
      },
      {}
    );
    cy.get('Button').should('be.disabled');
  });

  it('should be disabled when loading is true', () => {
    mountChatDeleteBtn(
      {
        messages: [{ message: 'Chat Message', isSent: false }],
        loading: true
      },
      {}
    );
    cy.get('Button').should('be.disabled');
  });

  // FIXME: da trovare soluzione per il click event
  // it('should emit clear event on click', () => {
  //   const clearMessagesSpy = cy.spy().as('clearMessagesSpy');

  //   mountChatDeleteBtn(
  //     {
  //       messages: [{ message: 'Chat Message', isSent: false }],
  //       loading: false
  //     },
  //     {
  //       'clear-messages': clearMessagesSpy
  //     }
  //   );

  //   // Verifica che il pulsante esista e simula il clic
  //   cy.get('Button')
  //     .should('exist')
  //     .click()
  //     .then((wrapper) => {
  //       //expect(wrapper.emitted('clear-messages')).to.have.length(1);

  //       cy.get('@vue').should(({ wrapper }) => {
  //         expect(wrapper.emitted('clear-messages')).to.have.length;
  //         expect(wrapper.emitted('clear-messages')[0][0]).to.equal('101');
  //       });
  //     });

  //   // Verifica che l'evento sia stato emesso
  //   cy.get('@clearMessagesSpy').should('have.been.called');
  // });
});
