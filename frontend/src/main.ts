import UtilsService from '@/services/utils.service';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import App from './App.vue';
import router from './router';

import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';

import BadgeDirective from 'primevue/badgedirective';
import Ripple from 'primevue/ripple';
import StyleClass from 'primevue/styleclass';
import Tooltip from 'primevue/tooltip';

// START import PrimeVue components (alphabetical order)
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
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
import ScrollPanel from 'primevue/scrollpanel';
import ScrollTop from 'primevue/scrolltop';
import SelectButton from 'primevue/selectbutton';
import Sidebar from 'primevue/sidebar';
import Slider from 'primevue/slider';
import TabMenu from 'primevue/tabmenu';
import Textarea from 'primevue/textarea';
import Toast from 'primevue/toast';
import ToggleButton from 'primevue/togglebutton';
// END import PrimeVue components (alphabetical order)

// locale files
import LocaleEn from '@/locales/en.json';
import LocaleIt from '@/locales/it.json';

import '@/assets/styles.scss';

type MessageSchema = typeof LocaleIt;

const i18n = createI18n<[MessageSchema], 'en' | 'it'>({
  legacy: false,
  locale: localStorage.getItem('language') ?? import.meta.env.VITE_DEFAULT_LANGUAGE ?? 'it',
  fallbackLocale: 'en',
  globalInjection: true,
  messages: {
    en: UtilsService.addCapitalizeValues(LocaleEn),
    it: UtilsService.addCapitalizeValues(LocaleIt)
  }
});

export default i18n;

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

// START PrimeVue components (alphabetical order)
app.component('PgAvatar', Avatar);
app.component('PgButton', Button);
app.component('PgCard', Card);
app.component('PgCheckbox', Checkbox);
app.component('PgColumn', Column);
app.component('PgDataTable', DataTable);
app.component('PgDialog', Dialog);
app.component('PgDivider', Divider);
app.component('PgDropdown', Dropdown);
app.component('PgFieldset', Fieldset);
app.component('PgFileUpload', FileUpload);
app.component('PgFloatLabel', FloatLabel);
app.component('PgInputGroup', InputGroup);
app.component('PgInputIcon', InputIcon);
app.component('PgInputSwitch', InputSwitch);
app.component('PgInputText', InputText);
app.component('PgPanel', Panel);
app.component('PgPassword', Password);
app.component('PgRadioButton', RadioButton);
app.component('PgSelectButton', SelectButton);
app.component('PgSidebar', Sidebar);
app.component('PgSlider', Slider);
app.component('PgTabMenu', TabMenu);
app.component('PgTextarea', Textarea);
app.component('PgToast', Toast);
app.component('PgToggleButton', ToggleButton);
app.component('PgScrollPanel', ScrollPanel);
app.component('PgScrollTop', ScrollTop);
// END PrimeVue components (alphabetical order)

app.mount('#app');
