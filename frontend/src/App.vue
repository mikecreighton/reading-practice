<style scoped lang="postcss"></style>

<template>
  <div class="App" :class="{ 'no-scroll': isModalOpen || isSettingsModalOpen }">
    <div class="app-content bg-background">
      <InputForm
        ref="inputFormRef"
        :settings="settings"
        :savedInputs="savedInputs"
        :preventScroll="isModalOpen || isSettingsModalOpen"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
        @storyGenerationError="handleStoryGenerationError"
        @openSettings="handleOpenSettings"
        @update:settings="saveSettings"
      />

      <div ref="storyModalContainer" class="hidden fixed inset-0 h-full w-full">
        <Transition @enter="onStoryModalEnter" @leave="onStoryModalLeave" @after-leave="onStoryModalAfterLeave">
          <StoryModal
            v-if="isModalOpen"
            :story="story"
            :illustration="illustration"
            :isLoading="isLoading"
            :wordList="wordList"
            :isError="isError"
            @regenerate="handleRegenerate"
            @closeRequest="handleStoryModalCloseRequest"
          />
        </Transition>
      </div>

      <div ref="settingsModalRef" class="hidden fixed inset-0 h-full w-full">
        <Transition @enter="onSettingsModalEnter" @leave="onSettingsModalLeave">
          <SettingsModal v-if="isSettingsModalOpen" v-model:settings="settings" @save="handleSettingsModalSave" />
        </Transition>
      </div>
    </div>

    <WelcomeScreen v-if="showWelcome" @getStarted="handleGetStarted" />
  </div>
</template>

<script setup>
import WelcomeScreen from "@/views/WelcomeScreen.vue"
import { ref, provide, onMounted, watch } from "vue"
import StoryModal from "@/views/StoryModal.vue"
import SettingsModal from "@/views/SettingsModal.vue"
import InputForm from "@/views/InputForm.vue"
import { detectOpenAI } from "@/services/ai"
import gsap from "gsap"
import { LOCAL_STORAGE_INPUTS_KEY, LOCAL_STORAGE_SETTINGS_KEY, DEFAULT_SETTINGS } from "./settings-constants"

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)
const isOpenAIAvailable = ref(false)
const isModalOpen = ref(false)
const isLoading = ref(false)
const isSettingsModalOpen = ref(false)
const settings = ref({ ...DEFAULT_SETTINGS })
const savedInputs = ref({})
const storyModalContainer = ref(null)
const settingsModalRef = ref(null)
const wordList = ref([])
const isError = ref(false)
const showWelcome = ref(true)

const loadSavedInputs = () => {
  const savedInputsData = localStorage.getItem(LOCAL_STORAGE_INPUTS_KEY)
  if (savedInputsData) {
    savedInputs.value = JSON.parse(savedInputsData)
  }
}

const loadSavedSettings = () => {
  const savedSettings = localStorage.getItem(LOCAL_STORAGE_SETTINGS_KEY)
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings)
  }
}

const MODAL_IN_DURATION = 0.4
const MODAL_IN_EASE = "expo.out"
const MODAL_OUT_DURATION = 0.35
const MODAL_OUT_EASE = "expo.inOut"

// Call this immediately
loadSavedInputs()
// Load settings from local storage
loadSavedSettings()

provide("isOpenAIAvailable", isOpenAIAvailable)

onMounted(() => {
  // Need to override this if we're just in debug mode.
  if (import.meta.env.VITE_DEBUG_INPUT_FORM === "true") {
    settings.value.gradeLevel = "2nd"
    settings.value.theme = "default"
  }

  detectOpenAI()
    .then((available) => {
      isOpenAIAvailable.value = available
    })
    .catch((error) => {
      console.warn("Problem detecting OpenAI availability:", error)
    })
})

const blurInputs = () => {
  const inputs = document.querySelectorAll("input, textarea")
  inputs.forEach((input) => {
    input.blur()
  })
}

const handleStoryGenerationStart = (formData) => {
  wordList.value = formData
  story.value = ""
  isModalOpen.value = true
  isLoading.value = true
  isError.value = false
  // We need to make sure that none of the inputs are currently focused or we wind up with a weird cursor bug
  blurInputs()
}

const handleStoryGenerationComplete = (generatedStory, generatedIllustration) => {
  story.value = generatedStory
  illustration.value = generatedIllustration
  isLoading.value = false
  isError.value = false
}

const handleStoryModalCloseRequest = () => {
  isModalOpen.value = false
  isLoading.value = false
}

const onStoryModalEnter = (el, done) => {
  storyModalContainer.value.classList.remove("hidden")

  gsap.from(el, {
    duration: MODAL_IN_DURATION,
    y: "100%",
    ease: MODAL_IN_EASE,
    onComplete: () => done(),
  })
}

const onStoryModalLeave = (el, done) => {
  inputFormRef.value.cancelRequest()
  gsap.to(el, {
    duration: MODAL_OUT_DURATION,
    y: "100%",
    ease: MODAL_OUT_EASE,
    onComplete: () => {
      storyModalContainer.value.classList.add("hidden")
      done()
    },
  })
}

const onStoryModalAfterLeave = () => {
  illustration.value = null
  story.value = null
}

const handleRegenerate = () => {
  inputFormRef.value.cancelRequest()
  illustration.value = null
  inputFormRef.value.submitForm()
}

const handleStoryGenerationError = (error) => {
  illustration.value = null
  isLoading.value = false
  story.value = error.message
  isError.value = true
}

const handleOpenSettings = () => {
  blurInputs()
  isSettingsModalOpen.value = true
}

const handleSettingsModalSave = (newSettings) => {
  isSettingsModalOpen.value = false
  saveSettings(newSettings)
}

const saveSettings = (newSettings) => {
  settings.value = newSettings
  localStorage.setItem(LOCAL_STORAGE_SETTINGS_KEY, JSON.stringify(settings.value))
}

const onSettingsModalEnter = (el, done) => {
  settingsModalRef.value.classList.remove("hidden")

  gsap.to(el, {
    duration: MODAL_IN_DURATION,
    y: "0",
    ease: MODAL_IN_EASE,
    onComplete: () => done(),
  })
}

const onSettingsModalLeave = (el, done) => {
  gsap.to(el, {
    duration: MODAL_OUT_DURATION,
    y: "100%",
    ease: MODAL_OUT_EASE,
    onComplete: () => {
      settingsModalRef.value.classList.add("hidden")
      done()
    },
  })
}

const handleGetStarted = () => {
  showWelcome.value = false
}

/**
 * Set the theme on the body element so that it can be used to set the entire
 * page's background color (for overscroll background behavior).
 */
watch(
  () => settings.value.theme,
  (newTheme) => {
    document.body.className = `bg-background theme-${newTheme}`
  },
  { immediate: true },
)
</script>
