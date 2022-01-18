import { createStore } from 'vuex'

export default createStore({
  state: {
    count: 0,
  },
  mutations: {
  count_up(state) {
    state.count += 1
  },
  },
  actions: {
  },
  modules: {
  }
})
