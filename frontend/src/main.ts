import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import PrimeVue from 'primevue/config';
import BadgeDirective from 'primevue/badgedirective';
import Button from 'primevue/button'
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import FloatLabel from 'primevue/floatlabel';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import RadioButton from 'primevue/radiobutton';
import Ripple from 'primevue/ripple';
import SelectButton from 'primevue/selectbutton';
import Sidebar from 'primevue/sidebar';
import StyleClass from 'primevue/styleclass';
import ToastService from 'primevue/toastservice';
import ToggleButton from 'primevue/togglebutton';
import Tooltip from 'primevue/tooltip';
import Slider from 'primevue/slider';
import FileUpload from 'primevue/fileupload';
import Checkbox from 'primevue/checkbox';
import InputSwitch from 'primevue/inputswitch';

import '@/assets/styles.scss';

const app = createApp(App);

app.use(router);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(DialogService);
app.use(ConfirmationService);

app.directive('tooltip', Tooltip);
app.directive('badge', BadgeDirective);
app.directive('ripple', Ripple);
app.directive('styleclass', StyleClass);


app.component('Button', Button);
app.component('FloatLabel', FloatLabel);
app.component('InputText', InputText);
app.component('InpitSwitch', InputSwitch);
app.component('Slider', Slider);
app.component('FileUpload', FileUpload);
app.component('ToggleButton', ToggleButton);
app.component('InputIcon', InputIcon);
app.component('SelectButton', SelectButton);
app.component('RadioButton', RadioButton);
app.component('Sidebar', Sidebar);
app.component('Checkbox', Checkbox);

app.mount('#app');
