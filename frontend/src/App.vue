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
const inputFormRef = ref(null)

const handleStoryGenerationStart = () => {
  story.value = " "
}

const handleStoryGenerationComplete = (generatedStory) => {
  story.value = generatedStory
}

const handleStoryModalCloseStart = () => {
  inputFormRef.value.cancelRequest()
}

const handleStoryModalCloseComplete = () => {
  story.value = null
}

const handleRegenerate = () => {
  inputFormRef.value.submitForm();
}

const handleStoryGenerationError = (error) => {
  story.value = error
}
</script>