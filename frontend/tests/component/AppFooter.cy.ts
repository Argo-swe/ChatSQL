import { createI18n } from 'vue-i18n';
import AppFooter from '../../src/components/layout/AppFooter.vue';

const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    globalInjection: true,
    message: 'Mock translation'
});

function mountAppFooter(props?) {
    return cy.mount(AppFooter, {
        global: {
            plugins: [i18n],
            mocks: {
                t: (key) => key
            },
        },
        props
    });
}

it('should emit clear event on click', () => {

    mountAppFooter(
    );

});
