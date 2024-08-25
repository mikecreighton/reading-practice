<style scoped lang="scss">
.button-labeled.active {
  /* Active state styles */
  background-color: #505050;
}
</style>
<template>
  <button
    :class="[
      'button-labeled',
      'btn',
      { active: isActive },
      customClass,
      { disabled: isDisabled },
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
