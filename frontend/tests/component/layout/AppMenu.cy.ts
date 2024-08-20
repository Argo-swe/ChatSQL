
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';
import AppMenu from '../../../src/components/layout/AppMenu.vue';

const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    globalInjection: true,
    message: 'Mock translation'
});

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/test', component: { template: '<div>Test</div>' } }
    ]
});

function mountAppMenu(props?) {
    return cy.mount(AppMenu, {
        global: {
            plugins: [i18n, router],
            mocks: {
                t: (key) => key
            },
        },
        props
    });
}

describe('AppMenu Component', () => {
    it('should display correctly', () => {
        mountAppMenu();

        cy.get('.layout-menu').should('be.visible');
        cy.get('.layout-menu').children().should('have.length.greaterThan', 0);
    });
});