import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';

import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import Button from "primevue/button"

const app = createApp(App)
app.component('Button', Button);

app.use(router)
app.use(PrimeVue)

app.mount('#app')