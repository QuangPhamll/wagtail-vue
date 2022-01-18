import { createApp } from 'vue'
import TodoItem from './components/TodoItem'
import store from './store'


const app = createApp({
  components: {
    TodoItem // Register for root level component
  },
}).use(store)

app.mount('#brahms-app')
