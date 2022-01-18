<template>
  <h3 class="f-weight">This is child component {{count}}</h3>
</template>

<script>
export default {
  name: "TodoItem2",
  props: {
    msg: String,
  },
  computed: {
    count() {
      return this.$store.state.count*2
    }
  }
}
</script>