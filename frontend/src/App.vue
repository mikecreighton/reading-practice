<template>
  <div class="App">
    <div class="app-content">
      <InputForm
        ref="inputFormRef"
        @storyPartReceived="handleStoryPartReceived"
        @storyGenerated="handleStoryGenerated"
      />
      <StoryModal
        v-if="story"
        :story="story"
        @regenerate="handleRegenerate"
        @closeComplete="handleStoryModalClosed"
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

const handleStoryGenerated = (generatedStory) => {
  story.value = generatedStory;
};

const handleStoryPartReceived = (storyPart) => {
  story.value = storyPart;
};

const handleStoryModalClosed = () => {
  story.value = null;
};

const handleRegenerate = () => {
  inputFormRef.value.cancelRequest();
  inputFormRef.value.submitForm();
};
</script>