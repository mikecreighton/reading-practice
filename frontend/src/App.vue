<style scoped style="postcss"></style>

<template>
  <div :class="['App', 'theme-' + settings.theme]">
    <div class="app-content bg-background">
      <InputForm
        ref="inputFormRef"
        :settings="settings"
        :savedInputs="savedInputs"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
        @storyGenerationError="handleStoryGenerationError"
        @openSettings="handleOpenSettings"
      />
      <Transition
        @enter="onStoryModalEnter"
        @leave="onStoryModalLeave"
        @after-leave="onStoryModalAfterLeave"
      >
        <StoryModal
          v-if="isModalOpen"
          :story="story"
          :illustration="illustration"
          :isLoading="isLoading"
          @regenerate="handleRegenerate"
          @closeRequest="handleStoryModalCloseRequest"
        />
      </Transition>
      <Transition
        @enter="onSettingsModalEnter"
        @leave="onSettingsModalLeave"
      >
        <SettingsModal
          v-if="isSettingsModalOpen"
          v-model:settings="settings"
          @save="handleSettingsModalSave"
        />
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted, watch } from "vue"
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
  gradeLevel: '2nd',
  theme: 'default'
})
const savedInputs = ref({})

const loadSavedInputs = () => {
  const savedInputsData = localStorage.getItem('userInputs')
  if (savedInputsData) {
    savedInputs.value = JSON.parse(savedInputsData)
  }
}

// Call this immediately
loadSavedInputs()

// Create a global variable to store the isOpenAIAvailable value
provide("isOpenAIAvailable", isOpenAIAvailable)

onMounted(() => {
  // Load settings from local storage
  const savedSettings = localStorage.getItem('userSettings')
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings)
  }

  detectOpenAI()
    .then((available) => {
      isOpenAIAvailable.value = available
    })
    .catch((error) => {
      // console.error("Error detecting OpenAI availability:", error)
    })
})
// Add this watch effect
watch(isSettingsModalOpen, (isOpen) => {
  if (isOpen) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
})

watch(isModalOpen, (isOpen) => {
  if (isOpen) {
    document.body.classList.add('modal-open')
  } else {
    document.body.classList.remove('modal-open')
  }
})

const handleStoryGenerationStart = () => {
  story.value = ""
  isModalOpen.value = true
  isLoading.value = true
}

const handleStoryGenerationComplete = (generatedStory, generatedIllustration) => {
  story.value = generatedStory
  illustration.value = generatedIllustration
  isLoading.value = false
}

const handleStoryModalCloseRequest = () => {
  isModalOpen.value = false
  isLoading.value = false
}

const onStoryModalEnter = (el, done) => {
  gsap.to(el, {
    duration: 0.5,
    y: "0",
    ease: Power4.easeOut,
    onComplete: () => done(),
  })
}

const onStoryModalLeave = (el, done) => {
  inputFormRef.value.cancelRequest()
  gsap.to(el, {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => done(),
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
}

const handleOpenSettings = () => {
  isSettingsModalOpen.value = true
}

const handleSettingsModalSave = () => {
  isSettingsModalOpen.value = false
  // Save settings to local storage
  localStorage.setItem('userSettings', JSON.stringify(settings.value))
  // You can add any additional logic here if needed
}

const onSettingsModalEnter = (el, done) => {
  gsap.to(el, {
    duration: 0.5,
    y: "0",
    ease: Power4.easeOut,
    onComplete: () => done(),
  })
}

const onSettingsModalLeave = (el, done) => {
  gsap.to(el, {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => done(),
  })
}
</script>
