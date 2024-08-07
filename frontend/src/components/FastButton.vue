<style scoped lang="scss">
.button-labeled {
  /* Base styles */
  font-size: 24px;
  width: auto;
  display: inline-block;
  padding: 24px 36px;
  cursor: pointer;
  user-select: none;
  border: none;
  color: #FFF;
  text-align: center;
  background-color: #101010;
  border-radius: 12px;
  transition: background-color 0.1s ease-in-out;
}

.button-labeled.active {
  /* Active state styles */
  background-color: #505050;
}

/* Responsive styles */
@media (max-width: 768px) {
  .button-labeled {
    font-size: 20px;
    padding: 20px 30px;
  }
}
@media (max-width: 480px) {
  .button-labeled {
    font-size: 16px;
    padding: 16px 24px;
  }
}
@media (max-width: 360px) {
  .button-labeled {
    font-size: 12px;
    padding: 12px 18px;
  }
}

</style>
<template>
    <button 
      :class="[
        'button-labeled',
        { active: isActive },
        customClass
      ]" 
      @touchstart.passive="activate" 
      @touchend.passive="deactivate"
      @touchcancel.passive="deactivate"
      @click.prevent="$emit('click')"
    >
      {{ buttonText }}
    </button>
  </template>
  
<script setup>
import { ref, defineProps } from 'vue'

const isActive = ref(false)

defineEmits(['click'])

defineProps({
  buttonText: {
    type: String,
    required: true
  },
  customClass: {
    type: [String, Array],
    required: false,
    default: ''
  }
})

const activate = () => {
  isActive.value = true
}

const deactivate = () => {
  isActive.value = false
}
</script>