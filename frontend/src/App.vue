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
import { ref } from 'vue'
import StoryModal from '@/views/StoryModal.vue'
import InputForm from '@/views/InputForm.vue'

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)

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