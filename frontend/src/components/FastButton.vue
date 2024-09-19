<style scoped></style>
<template>
  <button
    ref="buttonRef"
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
      'py-3 px-4 rounded-lg md:text-xl',
      customClass,
    ]"
    @touchstart.prevent="onTouchStart"
    @touchmove.prevent="onTouchMove"
    @touchend.prevent="onClick"
    @click.prevent="onClick"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"

const buttonRef = ref(null)
const startX = ref(0)
const startY = ref(0)
const touchEvents = ref([])

const props = defineProps({
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
  name: {
    type: String,
    required: false,
    default: "FastButton",
  },
})
const emit = defineEmits(["click"])

const addListener = (el, type, listener, useCapture) => {
  el.addEventListener(type, listener, useCapture)
  return {
    destroy: () => el.removeEventListener(type, listener, useCapture),
  }
}

const onTouchStart = (event) => {
  event.stopPropagation()
  touchEvents.value.push(
    addListener(buttonRef.value, "touchend", onClick, false),
    addListener(document.body, "touchmove", onTouchMove, false),
  )
  startX.value = event.touches[0].clientX
  startY.value = event.touches[0].clientY
}

const onTouchMove = (event) => {
  if (
    Math.abs(event.touches[0].clientX - startX.value) > 10 ||
    Math.abs(event.touches[0].clientY - startY.value) > 10
  ) {
    reset()
  }
}

const onClick = (event) => {
  event.stopPropagation()
  reset()
  if (!props.isDisabled) {
    if (event.type === "touchend") {
      // We need to make sure that the touch up event is inside of the button.
      const x = event.changedTouches[0].clientX
      const y = event.changedTouches[0].clientY
      // Check if the x and y are within the button's bounds.
      const rect = buttonRef.value.getBoundingClientRect()
      if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
        emit("click", event)
      }
    } else {
      emit("click", event)
    }
  }
  if (event.type === "touchend") {
    preventGhostClick(startX.value, startY.value)
  }
}

const reset = () => {
  touchEvents.value.forEach((event) => event.destroy())
  touchEvents.value = []
}

const coordinates = ref([])

const preventGhostClick = (x, y) => {
  coordinates.value.push(x, y)
  setTimeout(() => {
    coordinates.value.splice(0, 2)
  }, 2500)
}

const onDocumentClick = (event) => {
  for (let i = 0; i < coordinates.value.length; i += 2) {
    const x = coordinates.value[i]
    const y = coordinates.value[i + 1]
    if (Math.abs(event.clientX - x) < 25 && Math.abs(event.clientY - y) < 25) {
      event.stopPropagation()
      event.preventDefault()
    }
  }
}

onMounted(() => {
  if ("ontouchstart" in window) {
    document.addEventListener("click", onDocumentClick, true)
  }
})

onUnmounted(() => {
  if ("ontouchstart" in window) {
    document.removeEventListener("click", onDocumentClick, true)
  }
})
</script>
