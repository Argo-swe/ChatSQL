import { createApp } from 'vue';
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

import Button from 'primevue/button'
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import Slider from 'primevue/slider';
import FileUpload from 'primevue/fileupload';
import ToggleButton from 'primevue/togglebutton';
import InputIcon from 'primevue/inputicon';
import SelectButton from 'primevue/selectbutton';
import RadioButton from 'primevue/radiobutton';
import Sidebar from 'primevue/sidebar';
import Checkbox from 'primevue/checkbox';
import Dropdown from 'primevue/dropdown';
import Dialog from 'primevue/dialog';
import Textarea from 'primevue/textarea';
import Toast from 'primevue/toast';

import '@/assets/styles.scss';


const app = createApp(App);

app.use(router);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(DialogService);
app.use(ConfirmationService);

app.directive('badge', BadgeDirective);
app.directive('tooltip', Tooltip);
app.directive('ripple', Ripple);
app.directive('styleclass', StyleClass);

app.component('Button', Button);
app.component('FloatLabel', FloatLabel);
app.component('InputText', InputText);
app.component('InputSwitch', InputSwitch);
app.component('Slider', Slider);
app.component('FileUpload', FileUpload);
app.component('ToggleButton', ToggleButton);
app.component('InputIcon', InputIcon);
app.component('SelectButton', SelectButton);
app.component('RadioButton', RadioButton);
app.component('Sidebar', Sidebar);
app.component('Checkbox', Checkbox);
app.component('Dropdown', Dropdown);
app.component('Dialog', Dialog);
app.component('Textarea', Textarea);
app.component('Toast', Toast);

app.mount('#app');
