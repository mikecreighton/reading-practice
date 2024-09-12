<style scoped lang="postcss">
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
          <div class="relative">
            <select
              id="gradeLevel"
              v-model="localSettings.gradeLevel"
              class="w-full py-3 px-4 border border-input-border text-primary bg-input-background focus:outline-none focus:border-input-border-focus rounded-md appearance-none"
            >
              <option v-for="grade in gradeOptions" :key="grade" :value="grade">{{ grade }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
              <i class="bi-chevron-down" style="position: absolute; right: 10px;"></i>
            </div>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-lg text-gray-800 mb-2">Theme</label>
          <div class="flex flex-col space-y-2">
            <button
              v-for="(value, key) in themeOptions"
              :key="key"
              @click="localSettings.theme = key"
              :class="['theme-button', 'text-primary', { active: localSettings.theme === key }]"
            >
              {{ value }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Bottom action buttons -->
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 px-10 py-5 bg-white drop-shadow-bar"
    >
      <div class="flex justify-end items-center max-w-[700px] mx-auto my-0">
        <FastButton @click="handleSave">Save</FastButton>
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

const emit = defineEmits(["update:settings", "save"])

const localSettings = ref({ ...props.settings })

// Watch for changes in localSettings and emit updates
watch(localSettings, (newSettings) => {
  emit('update:settings', newSettings)
}, { deep: true })

const themeOptions = {
  'default': 'Default',
  'bubblegum': 'Bubblegum',
  'adventure': 'Adventure'
}

const gradeOptions = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']

const handleSave = () => {
  emit('save')
}
</script>