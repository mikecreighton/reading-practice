<template>
  <div class="App">
    <div class="app-content">
      <InputForm
        ref="inputFormRef"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
        @storyGenerationError="handleStoryGenerationError"
      />
      <StoryModal
        v-if="story"
        :story="story"
        :illustration="illustration"
        @regenerate="handleRegenerate"
        @closeStart="handleStoryModalCloseStart"
        @closeComplete="handleStoryModalCloseComplete"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'
import StoryModal from '@/views/StoryModal.vue'
import InputForm from '@/views/InputForm.vue'
import { detectOpenAI } from '@/services/ai';

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)
const isOpenAIAvailable = ref(false)

// Create a global variable to store the isOpenAIAvailable value
provide('isOpenAIAvailable', isOpenAIAvailable)

onMounted(() => {
  detectOpenAI().then((available) => {
    isOpenAIAvailable.value = available
  }).catch((error) => {
    // console.error("Error detecting OpenAI availability:", error)
  })
})

const handleStoryGenerationStart = () => {
  story.value = " "
}

const handleStoryGenerationComplete = (generatedStory, generatedIllustration) => {
  story.value = generatedStory
  illustration.value = generatedIllustration
}

const handleStoryModalCloseStart = () => {
  inputFormRef.value.cancelRequest()
}

const handleStoryModalCloseComplete = () => {
  illustration.value = null
  story.value = null
}

const handleRegenerate = () => {
  inputFormRef.value.cancelRequest();
  illustration.value = null
  inputFormRef.value.submitForm();
}

const handleStoryGenerationError = (error) => {
  story.value = error
}
</script>