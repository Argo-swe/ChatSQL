import { createI18n } from 'vue-i18n';
import AppTopbar from '../../../src/components/layout/AppTopbar.vue';

const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    globalInjection: true,
    message: 'Mock translation'
});


function mountAppTopbar(props?) {
    return cy.mount(AppTopbar, {
        global: {
            plugins: [i18n],
            mocks: {
                t: (key) => key
            },
        },
        props
    });
}

describe('AppTopbar Component', () => {
    it('should display correctly', () => {
        mountAppTopbar();

        cy.get('.layout-topbar').should('be.visible');
    });
});