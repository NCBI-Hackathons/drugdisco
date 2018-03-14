<template>
<div class="index">
  <el-form ref="form" :model="form" label-width="250px">
    <el-form-item label="Receptor">
      <input type="file" ref="rec_file">
    </el-form-item>

    <!--<el-form-item label="Ligand">
      <input type="file" ref="lig_file">
    </el-form-item>-->

    <el-form-item label="Reference molecule">
      <input type="file" ref="ref_file">
    </el-form-item>

	<el-form-item label="Mail">
      <el-input v-model="form.mail"></el-input>
    </el-form-item>
	
    <el-form-item label="">
      <a href="#" @click.prevent="show_options^=true">{{show_options?'Hide':'Show'}} options</a>
    </el-form-item>

    <el-form-item label="Allow ROTAMER mode of ligand" v-show="show_options">
      <el-switch v-model="form.allow_rotamer"></el-switch>
    </el-form-item>

    <el-form-item label="Perform backrub minimization" v-show="show_options">
      <el-switch v-model="form.perform_backrub"></el-switch>
    </el-form-item>

    <el-form-item label="Potential type" v-show="show_options">
      <el-select v-model="form.potential" placeholder="Potential Type">
        <el-option
          v-for="item in potential_options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="Constraints" v-show="show_options">
      <el-input type="textarea" :rows="5" v-model="form.constraints"></el-input>
    </el-form-item>

    <el-form-item label="Cutoff" v-show="show_options">
      <el-input v-model="form.cutoff"></el-input>
    </el-form-item>

    <el-form-item label="Number of poses to explore" v-show="show_options">
      <el-input v-model="form.num_poses"></el-input>
    </el-form-item>

    <el-form-item label="Seed" v-show="show_options">
      <el-input v-model="form.seed"></el-input>
    </el-form-item>

    <el-form-item>
      <el-button @click="onSubmit" type="primary">Submit</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
import axios from 'axios'

axios.defaults.headers.post['Content-Type'] = 'multipart/form-data'

export default {
  name: 'Index',
  data () {
    return {
      show_options: false,
      potential_options: [{
        value: 'spring',
        label: 'Spring Potential'
      }, {
        value: 'squarewell',
        label: 'Square Well Potential'
      }],
      form: {
        num_poses: 1,
        potential: 'spring',
        constraints: '',
        allow_rotamer: true,
        perform_backrub: false,
        cutoff: 10,
        seed: 1
      }
    }
  },
  methods: {
    onSubmit () {
      var formData = new FormData()
      for (var i in this.form) {
        formData.append(i, this.form[i])
      }
      formData.append('rec_file', this.$refs.rec_file.files[0])
      // formData.append('lig_file', this.$refs.lig_file.files[0])
      formData.append('ref_file', this.$refs.ref_file.files[0])

      axios.post('submit', formData).then(response => {
        console.log('OK!')
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
