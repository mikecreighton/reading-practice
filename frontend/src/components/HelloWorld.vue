<style lang="scss" scoped>

</style>
<template>
  <div class="container mt-5">
    <h1 class="mb-4">Welcome to My Vue + Bootstrap App</h1>
    
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Card Example</h5>
            <p class="card-text">This is an example of a Bootstrap card in a Vue component.</p>
            <button class="btn btn-primary" @click="incrementCounter">
              Clicked {{ counter }} times
            </button>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <form>
          <div class="mb-3">
            <label for="exampleInput" class="form-label">Example input</label>
            <input type="text" class="form-control" id="exampleInput" v-model="inputText">
          </div>
          <div class="mb-3">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="exampleCheck" v-model="isChecked">
              <label class="form-check-label" for="exampleCheck">Check me out</label>
            </div>
          </div>
          <button type="submit" class="btn btn-success" @click.prevent="submitForm">Submit</button>
        </form>
      </div>
    </div>
    
    <div class="alert alert-info mt-4" role="alert" v-if="showAlert">
      Form submitted! Input: {{ inputText }}, Checked: {{ isChecked }}
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'

const counter = ref(0)
const inputText = ref('')
const isChecked = ref(false)
const showAlert = ref(false)

const incrementCounter = () => {
  counter.value++
}

const submitForm = () => {
  showAlert.value = true
  // Here you would typically handle the form submission
  console.log('Form submitted! Input:', inputText.value, 'Checked:', isChecked.value)
}
</script>