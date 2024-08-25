<template>
  <button
    :class="[
      {
        'bg-primary border border-primary text-white hover:bg-gray-900 hover:border-gray-900':
          type === 'primary',
      },
      {
        'border border-secondary text-gray-800 hover:bg-gray-300 hover:text-gray-900 hover:border-gray-900':
          type === 'secondary',
      },
      { 'opacity-50 cursor-not-allowed': isDisabled },
      'py-3 px-4 rounded-lg',
      customClass,
    ]"
    @touchstart.passive="activate"
    @touchend.passive="deactivate"
    @touchcancel.passive="deactivate"
    @click.prevent="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { ref } from "vue"

const isActive = ref(false)

defineEmits(["click"])

defineProps({
  customClass: {
    type: [String, Array],
    required: false,
    default: "",
  },
  type: {
    type: String,
    required: false,
    default: "primary",
  },
  isDisabled: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const activate = () => {
  isActive.value = true
}

const deactivate = () => {
  isActive.value = false
}
</script>

<style scoped>
/* Remove all styles here, as they're now handled by Tailwind classes */
</style>
