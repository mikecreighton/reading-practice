<style scoped lang="postcss"></style>

<template>
  <div class="settings-modal fixed inset-0 translate-y-full bg-background w-full overflow-hidden h-[100dvh]">
    <div class="settings-content h-full overflow-y-auto pb-[104px]">
      <div class="max-w-[700px] w-full mx-auto p-10 md:p-[60px_40px_100px_40px]">
        <h2 class="text-2xl md:text-4xl font-bold mb-10 text-text tracking-tight">Settings</h2>

        <div class="mb-6 md:mb-10">
          <label class="block text-xl md:text-3xl text-text mb-3 md:mb-4" for="gradeLevel">Grade Level</label>
          <div class="relative">
            <select
              id="gradeLevel"
              v-model="localSettings.gradeLevel"
              class="w-full py-3 px-4 md:text-2xl border border-2 border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus rounded-lg appearance-none"
            >
              <option v-for="grade in gradeOptions" :key="grade" :value="grade">{{ grade }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-input-text">
              <i class="bi-chevron-down absolute right-4 top-4 md:top-5"></i>
            </div>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-xl md:text-3xl text-text mb-3 md:mb-4">Theme</label>
          <div class="flex flex-col space-y-3">
            <button
              v-for="(value, key) in themeOptions"
              :key="key"
              @click="localSettings.theme = key"
              :class="[
                'border border-2 py-3 px-4 rounded-lg md:text-2xl',
                {
                  'bg-button-option text-button-option-text border-button-option-border hover:text-button-option-hover-text hover:bg-button-option-hover hover:border-button-option-hover-border':
                    localSettings.theme !== key,
                },
                {
                  'bg-button-option-selected text-button-option-selected-text border-button-option-selected-border':
                    localSettings.theme === key,
                },
              ]"
            >
              <i v-if="localSettings.theme === key" class="bi-check relative top-[1px] md:top-[2px]"></i>
              {{ value }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Bottom action buttons -->
    <div class="action-buttons-container fixed bottom-0 left-0 right-0 bg-bottom-bar drop-shadow-bar">
      <div class="flex justify-end items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <FastButton name="Save" @click="handleSave">Save</FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import FastButton from "@/components/FastButton.vue"
import { onMounted, onUnmounted } from "vue"

const props = defineProps({
  settings: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(["update:settings", "save"])

const localSettings = ref({ ...props.settings })

// Watch for changes in localSettings and emit updates
watch(
  localSettings,
  (newSettings) => {
    emit("update:settings", newSettings)
  },
  { deep: true },
)

const themeOptions = {
  default: "Default",
  bubblegum: "Bubblegum",
  adventure: "Adventure",
}

const gradeOptions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]

const handleSave = () => {
  // Save settings to local storage
  localStorage.setItem("userSettings", JSON.stringify(localSettings.value))
  emit("save")
}

/**
 * All of this garbage below is to prevent the page from scrolling when the modal is open on Mobile Safari.
 */

const preventScroll = (e) => {
  e.preventDefault()
}

const disableScroll = () => {
  document.addEventListener("touchmove", preventScroll, { passive: false })
}

const enableScroll = () => {
  document.removeEventListener("touchmove", preventScroll)
}

onMounted(() => {
  disableScroll()
})

onUnmounted(() => {
  enableScroll()
})
</script>
