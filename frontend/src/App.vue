<style scoped></style>

<template>
  <div class="App">
    <div class="app-content bg-white">
      <InputForm
        ref="inputFormRef"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
        @storyGenerationError="handleStoryGenerationError"
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
          @regenerate="handleRegenerate"
          @closeRequest="handleStoryModalCloseRequest"
        />
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from "vue"
import StoryModal from "@/views/StoryModal.vue"
import InputForm from "@/views/InputForm.vue"
import { detectOpenAI } from "@/services/ai"
import gsap, { Power4 } from "gsap"

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)
const isOpenAIAvailable = ref(false)
const isModalOpen = ref(false)

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
}

const handleStoryGenerationComplete = (generatedStory, generatedIllustration) => {
  story.value = generatedStory
  illustration.value = generatedIllustration
}

const handleStoryModalCloseRequest = () => {
  isModalOpen.value = false
}

const onStoryModalEnter = (el, done) => {
  gsap.to(el, {
    duration: 0.5,
    y: "0%",
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
  story.value = error
}
</script>
