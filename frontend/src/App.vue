<style scoped lang="postcss">
/*
  This keeps the content that sits below all modals from scrolling on Mobile Safari because of its
  "overscroll" behavior.
 */
.no-scroll {
  @apply overflow-hidden h-full max-h-full touch-none;
}
</style>

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
import { ref, provide, onMounted, watch, nextTick } from "vue"
import StoryModal from "@/views/StoryModal.vue"
import SettingsModal from "@/views/SettingsModal.vue"
import InputForm from "@/views/InputForm.vue"
import { detectOpenAI } from "@/services/ai"
import gsap, { Power4 } from "gsap"

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)
const isOpenAIAvailable = ref(false)
const isModalOpen = ref(false)
const isLoading = ref(false)
const isSettingsModalOpen = ref(false)
const settings = ref({
  gradeLevel: "2nd",
  theme: "default",
})
const savedInputs = ref({})
const storyModalContainer = ref(null)
const settingsModalRef = ref(null)
const wordList = ref([])
const isError = ref(false)
const showWelcome = ref(true)

const loadSavedInputs = () => {
  const savedInputsData = localStorage.getItem("userInputs")
  if (savedInputsData) {
    savedInputs.value = JSON.parse(savedInputsData)
  }
}

const MODAL_IN_DURATION = 0.4
const MODAL_IN_EASE = "expo.out"
const MODAL_OUT_DURATION = 0.35
const MODAL_OUT_EASE = "expo.inOut"

// Call this immediately
loadSavedInputs()

provide("isOpenAIAvailable", isOpenAIAvailable)

onMounted(() => {
  // Load settings from local storage
  const savedSettings = localStorage.getItem("userSettings")
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings)
  }

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

// const setBodyOverflow = (isHidden) => {
//   // document.body.style.overflow = isHidden ? "hidden" : ""
// }

// watch(isSettingsModalOpen, (isOpen) => {
//   if (isOpen) {
//     document.body.classList.add("modal-open")
//     nextTick(() => setBodyOverflow(true))
//   } else {
//     document.body.classList.remove("modal-open")
//     nextTick(() => setBodyOverflow(false))
//   }
// })

// watch(isModalOpen, (isOpen) => {
//   if (isOpen) {
//     document.body.classList.add("modal-open")
//     nextTick(() => setBodyOverflow(true))
//   } else {
//     document.body.classList.remove("modal-open")
//     nextTick(() => setBodyOverflow(false))
//   }
// })

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

const handleSettingsModalSave = () => {
  isSettingsModalOpen.value = false
  localStorage.setItem("userSettings", JSON.stringify(settings.value))
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

// Add this watch effect
watch(
  () => settings.value.theme,
  (newTheme) => {
    document.body.className = `bg-background theme-${newTheme}`
  },
  { immediate: true },
)
</script>
