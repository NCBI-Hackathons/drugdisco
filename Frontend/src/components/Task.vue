<template>
<div class="task">
  Task details.
  {{$route.params.id}}
</div>
</template>

<script>
import axios from 'axios'

axios.defaults.headers.post['Content-Type'] = 'multipart/form-data'

export default {
  name: 'Task',
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.el-form-item {
  margin-bottom: 3px;
}

</style>
