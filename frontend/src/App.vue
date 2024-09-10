<style scoped></style>

<template>
  <div class="App">
    <div class="app-content bg-white">
      <InputForm
        ref="inputFormRef"
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
          @close="handleSettingsModalClose"
          @cancel="handleSettingsModalCancel"
        />
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from "vue"
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

// Create a global variable to store the isOpenAIAvailable value
provide("isOpenAIAvailable", isOpenAIAvailable)

onMounted(() => {
  detectOpenAI()
    .then((available) => {
      isOpenAIAvailable.value = available
    })
    .catch((error) => {
      // console.error("Error detecting OpenAI availability:", error)
    })
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
  console.log("error:", error)
  illustration.value = null
  isLoading.value = false
  story.value = error
}

const handleOpenSettings = () => {
  isSettingsModalOpen.value = true
}

const handleSettingsModalClose = () => {
  isSettingsModalOpen.value = false
}

const handleSettingsModalCancel = () => {
  isSettingsModalOpen.value = false
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

const onSettingsModalAfterLeave = () => {
  illustration.value = null
  story.value = null
}
</script>
