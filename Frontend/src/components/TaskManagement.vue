<template>
<div class="taskmanagement">
  <el-table :data="tableData3" height="800" style="width: 100%">
    <el-table-column prop="date" label="Date" width="180"></el-table-column>
    <el-table-column prop="name" label="Name" width="180"></el-table-column>
    <el-table-column prop="address" label="Address"></el-table-column>
  </el-table>
</div>
</template>

<script>
import axios from 'axios'

axios.defaults.headers.post['Content-Type'] = 'multipart/form-data'

export default {
  name: 'TaskManagement',
  data () {
    return {
      tableData3: [{
        date: '2016-05-03',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-02',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-04',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-01',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-08',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-06',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }, {
        date: '2016-05-07',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles'
      }]
    }
  },
  methods: {
    onSubmit () {
      var formData = new FormData()
      for (var i in this.form) {
        formData.append(i, this.form[i])
      }
      formData.append('rec_file', this.$refs.rec_file.files[0])
      formData.append('lig_file', this.$refs.lig_file.files[0])
      formData.append('ref_file', this.$refs.ref_file.files[0])
      axios.post('submit', formData).then(response => {
        console.log(response)
      }).catch(() => {
        console.log('post failed')
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.el-form-item {
  margin-bottom: 3px;
}

</style>
