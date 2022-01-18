<template>
  <h3>{{msg}} <img src="../assets/logo.png" alt="..." height="40"></h3>
  <button type="button" @click="count_up()">Count up</button>
  <div> upper {{count}}</div>
  <TodoItem2></TodoItem2>
</template>

<script>
import TodoItem2 from "@/components/TodoItem2";
export default {
  name: "TodoItem",
  components:  {
    TodoItem2
  },
  props: {
    msg: String,
  },
  computed: {
    count() {
      return this.$store.state.count
    }
  },
  methods: {
    count_up() {
      this.$store.commit('count_up')
    }
  }
}
</script>