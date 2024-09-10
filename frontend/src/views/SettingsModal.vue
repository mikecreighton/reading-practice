<style scoped>
.theme-button {
  @apply py-3 px-4 rounded-lg text-lg w-full text-left;
}
.theme-button.active {
  @apply bg-input-background border border-input-border-focus;
}
.theme-button:not(.active) {
  @apply bg-white border border-input-border;
}
</style>

<template>
  <div class="absolute top-0 left-0 right-0 translate-y-full bg-white h-[100vh] w-full">
    <div class="settings-wrapper pb-[104px] overflow-y-scroll absolute w-full h-full top-0">
      <div class="p-10 md:p-[60px_40px_100px_40px]">
        <h2 class="text-2xl md:text-3xl font-bold mb-6">Settings</h2>
        
        <div class="mb-6">
          <label class="block text-lg text-gray-800 mb-2" for="gradeLevel">Grade Level</label>
          <select
            id="gradeLevel"
            v-model="localSettings.gradeLevel"
            class="w-full py-3 px-4 border border-input-border bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
          >
            <option v-for="grade in gradeOptions" :key="grade" :value="grade">{{ grade }}</option>
          </select>
        </div>

        <div class="mb-6">
          <label class="block text-lg text-gray-800 mb-2">Theme</label>
          <div class="flex flex-col space-y-2">
            <button
              v-for="theme in themeOptions"
              :key="theme"
              @click="localSettings.theme = theme"
              :class="['theme-button', { active: localSettings.theme === theme }]"
            >
              {{ theme }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Bottom action buttons -->
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 px-10 py-5 bg-white drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] mx-auto my-0">
        <FastButton type="secondary" @click="handleCancel">Cancel</FastButton>
        <FastButton @click="handleClose">Close</FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import FastButton from "@/components/FastButton.vue"

const props = defineProps({
  settings: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(["close", "cancel", "update:settings"])

const localSettings = ref({ ...props.settings })

const gradeOptions = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']
const themeOptions = ['Default', 'Bubblegum', 'Adventure']

watch(() => props.settings, (newSettings) => {
  localSettings.value = { ...newSettings }
}, { deep: true })

const handleClose = () => {
  emit('update:settings', localSettings.value)
  emit('close')
}

const handleCancel = () => {
  emit('cancel')
}
</script>