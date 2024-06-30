import { createApp } from 'vue';
import { createI18n } from 'vue-i18n'
import UtilsService from '@/services/utils.service'
import App from './App.vue';
import router from './router';

import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import DialogService from 'primevue/dialogservice';
import ConfirmationService from 'primevue/confirmationservice';

import BadgeDirective from 'primevue/badgedirective';
import Tooltip from 'primevue/tooltip';
import Ripple from 'primevue/ripple';
import StyleClass from 'primevue/styleclass';

// import PrimeVue components (alphabetical order)
import Avatar from 'primevue/avatar';
import Button from 'primevue/button'
import Card from 'primevue/card';
import Checkbox from 'primevue/checkbox';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Dialog from 'primevue/dialog';
import Divider from 'primevue/divider';
import Dropdown from 'primevue/dropdown';
import Fieldset from 'primevue/fieldset';
import FileUpload from 'primevue/fileupload';
import FloatLabel from 'primevue/floatlabel';
import InputGroup from 'primevue/inputgroup';
import InputIcon from 'primevue/inputicon';
import InputSwitch from 'primevue/inputswitch';
import InputText from 'primevue/inputtext';
import Panel from 'primevue/panel';
import Password from 'primevue/password';
import RadioButton from 'primevue/radiobutton';
import SelectButton from 'primevue/selectbutton';
import Sidebar from 'primevue/sidebar';
import Slider from 'primevue/slider';
import TabMenu from 'primevue/tabmenu';
import Textarea from 'primevue/textarea';
import Toast from 'primevue/toast';
import ToggleButton from 'primevue/togglebutton';
import ScrollTop from 'primevue/scrolltop';
// END import PrimeVue components (alphabetical order)

// locale files
import LocaleEn from '@/locales/en.json'
import LocaleIt from '@/locales/it.json'

import '@/assets/styles.scss';

type MessageSchema = typeof LocaleIt

const i18n = createI18n<[MessageSchema], 'en' | 'it' >({
    legacy: false,
    locale: localStorage.getItem('language') ?? import.meta.env.VITE_DEFAULT_LANGUAGE ?? 'it',
    fallbackLocale: 'en',
    globalInjection: true,
    messages: {
        en: UtilsService.addCapitalizeValues(LocaleEn),
        it: UtilsService.addCapitalizeValues(LocaleIt)
    }
})

const app = createApp(App);

app.use(router);
app.use(i18n);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(DialogService);
app.use(ConfirmationService);

app.directive('badge', BadgeDirective);
app.directive('tooltip', Tooltip);
app.directive('ripple', Ripple);
app.directive('styleclass', StyleClass);

// PrimeVue components (alphabetical order)
app.component('Avatar', Avatar);
app.component('Button', Button);
app.component('Card', Card);
app.component('Checkbox', Checkbox);
app.component('Column', Column);
app.component('DataTable', DataTable);
app.component('Dialog', Dialog);
app.component('Divider', Divider);
app.component('Dropdown', Dropdown);
app.component('Fieldset', Fieldset);
app.component('FileUpload', FileUpload);
app.component('FloatLabel', FloatLabel);
app.component('InputGroup', InputGroup);
app.component('InputIcon', InputIcon);
app.component('InputSwitch', InputSwitch);
app.component('InputText', InputText);
app.component('Panel', Panel);
app.component('Password', Password);
app.component('RadioButton', RadioButton);
app.component('SelectButton', SelectButton);
app.component('Sidebar', Sidebar);
app.component('Slider', Slider);
app.component('TabMenu', TabMenu);
app.component('Textarea', Textarea);
app.component('Toast', Toast);
app.component('ToggleButton', ToggleButton);
app.component('ScrollTop', ScrollTop);
// END PrimeVue components (alphabetical order)

app.mount('#app');
