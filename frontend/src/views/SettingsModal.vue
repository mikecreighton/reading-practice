<style scoped lang="postcss">
.settings-content {
  -webkit-overflow-scrolling: touch;
}
</style>

<template>
  <div class="settings-modal fixed inset-0 translate-y-full bg-background w-full overflow-hidden h-[100dvh]">
    <div class="settings-content h-full overflow-y-auto pb-[104px]">
      <div class="max-w-[700px] w-full mx-auto p-10 md:p-[60px_40px_100px_40px]">
        <h2 class="text-2xl md:text-4xl font-bold mb-10 text-text tracking-tight">Settings</h2>

        <div class="mb-6">
          <label class="block text-xl md:text-3xl text-text mb-3 md:mb-4">Theme</label>
          <div class="flex flex-col space-y-3">
            <button
              v-for="(value, key) in themeOptions"
              :key="key"
              @click="settings.theme = key"
              :class="[
                'border-2 py-3 px-4 rounded-lg md:text-2xl',
                {
                  'bg-button-option text-button-option-text border-button-option-border hover:text-button-option-hover-text hover:bg-button-option-hover hover:border-button-option-hover-border':
                    settings.theme !== key,
                },
                {
                  'bg-button-option-selected text-button-option-selected-text border-button-option-selected-border':
                    settings.theme === key,
                },
              ]"
            >
              <i v-if="settings.theme === key" class="bi-check relative top-[1px] md:top-[2px]"></i>
              {{ value }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Bottom action buttons -->
    <div class="action-buttons-container fixed bottom-0 left-0 right-0 bg-bottom-bar drop-shadow-bar">
      <div class="flex justify-end items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <FastButton name="Save" @click="emit('save')">Save</FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineModel } from "vue"
import FastButton from "@/components/FastButton.vue"
import { onMounted, onUnmounted } from "vue"

const settings = defineModel("settings")
const emit = defineEmits(["save"])

const themeOptions = {
  default: "Default",
  bubblegum: "Bubblegum",
  adventure: "Adventure",
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
