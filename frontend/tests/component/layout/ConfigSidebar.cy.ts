import { createI18n } from 'vue-i18n';
import ConfigSidebar from '../../../src/components/layout/ConfigSidebar.vue';
import { usePrimeVue } from 'primevue/config';
import { useLayout } from '../../../src/composables/layout';


const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    globalInjection: true,
    message: 'Mock translation'
});

const { setScale, layoutConfig, layoutState } = useLayout();

function mountConfigSidebar(props?) {
    return cy.mount(ConfigSidebar, {
        global: {
            plugins: [i18n, layoutState],
            mocks: {
                t: (key) => key
            },
        },
        props
    });
}

describe('ConfigSidebar Component', () => {
    it('should display correctly', () => {
        mountConfigSidebar();

        cy.get('.layout-config-sidebar').should('be.visible');
    });
});
