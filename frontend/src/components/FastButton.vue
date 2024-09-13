<style scoped></style>
<template>
  <button
    :class="[
      {
        'border text-button-primary-text bg-button-primary border-button-primary-border hover:bg-button-primary-hover hover:border-button-primary-border':
          type === 'primary',
      },
      {
        'border text-button-secondary-text bg-button-secondary border-button-secondary-border hover:text-button-secondary-hover-text hover:bg-button-secondary-hover hover:border-button-secondary-hover-border':
          type === 'secondary',
      },
      { 'opacity-40 cursor-not-allowed': isDisabled },
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
