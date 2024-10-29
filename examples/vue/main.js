import { createApp } from 'vue';
import App from './App.vue';
import StatCollector from './StatCollector';

const app = createApp(App);

app.use(StatCollector, {
  apiKey: 'your-api-key'
});

app.mount('#app');
