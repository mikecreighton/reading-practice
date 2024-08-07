<template>
  <div class="App">
    <div class="app-content">
      <InputForm
        ref="inputFormRef"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
      />
      <StoryModal
        v-if="story"
        :story="story"
        @regenerate="handleRegenerate"
        @closeComplete="handleStoryModalClose"
        @cancelRequest="inputFormRef.cancelRequest"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import StoryModal from './components/StoryModal.vue';
import InputForm from './components/InputForm.vue';

const story = ref(null);
const inputFormRef = ref(null);

const handleStoryGenerationStart = () => {
  story.value = " ";
};

const handleStoryGenerationComplete = (generatedStory) => {
  story.value = generatedStory;
};

const handleStoryModalClose = () => {
  story.value = null;
};

const handleRegenerate = () => {
  inputFormRef.value.cancelRequest();
  inputFormRef.value.submitForm();
};
</script>