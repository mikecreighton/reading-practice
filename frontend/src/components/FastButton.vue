<template>
  <button
    :class="[
      'button-labeled',
      { 'bg-gray-700': isActive },
      customClass,
      { 'opacity-50 cursor-not-allowed': isDisabled },
      'py-3',
      'px-4',
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
