<style lang="scss" scoped>
form {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    max-width: 700px;
    padding: 40px 40px;
    background-color: #fff;

    label {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-bottom: 30px;
        font-size: 1.2rem;
        color: #333;

        .helper {
            color: #AAA;
            display: inline;
            font-size: 80%;
        }
    }

    input {
        margin-top: 12px;
        height: 60px;
        line-height: 40px;
        padding: 0 20px;
        font-size: 20px;
        border-radius: 4px;
        border: 1px solid #AAA;
        background-color: #F0F0F0;
        color: #333;
    }

    input.slider {
        appearance: none;
        width: 100%;
        height: 40px;
        border-radius: 6px;
        border: 0 none;
        background: #101010;
        outline: none;
        transition: opacity .2s;

        &::-webkit-slider-thumb {
            appearance: none;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #FFF;
            cursor: pointer;
        }

        &:focus {
            touch-action: manipulation;
        }
    }

    // make the buttons sit side-by-side
    .buttons-container {
        display: flex;
        justify-content: flex-end;
        gap: 20px;
        width: 100%;

        @media (max-width: 768px) {
            gap: 16px;
        }
        @media (max-width: 480px) {
            gap: 12px;
            justify-content: space-between;
        }
        @media (max-width: 375px) {
            gap: 8px;
        }
    }
}
</style>
<template>
  <form>
    <label>
      <span class="prevent-wrap">
        Words to Include in the Story
        <span class="helper">(comma-separated)</span>
      </span>
      <input
        type="text"
        v-model="words"
      />
    </label>
    <label>
      The Story's Main Character
      <input
        type="text"
        v-model="characterName"
      />
    </label>
    <label>
      Where the Story Takes Place
      <input
        type="text"
        v-model="setting"
      />
    </label>
    <label>
      Humor Level
      <input
        type="range"
        min="1"
        max="10"
        v-model="humor"
        class="slider"
      />
    </label>
    <div class="buttons-container">
      <FastButton :disabled="isLoading" buttonText="Generate Story" @click="handleSubmit"></FastButton>
      <FastButton buttonText="Reset" @click="handleReset"></FastButton>
    </div>
  </form>
</template>

<script setup>
import { ref, inject } from 'vue'
import FastButton from '@/components/FastButton.vue'
import { generateStory, generateIllustration } from '@/services/ai'

const DEBUG_STORY_GENERATION = ref(true)
const DEFAULT_HUMOR_VALUE = 3

const words = ref('')
const characterName = ref('')
const setting = ref('')
const humor = ref(DEFAULT_HUMOR_VALUE)
const isLoading = ref(false)
const abortController = ref(null)
const isOpenAIAvailable = inject('isOpenAIAvailable')

const emit = defineEmits(['storyGenerationStart', 'storyGenerationComplete', 'storyGenerationError'])

if (DEBUG_STORY_GENERATION.value) {
  words.value = 'friend, because, weather, bicycle, favorite'
  characterName.value = 'The Big Bad Wolf'
  setting.value = 'A school bus'
  humor.value = 10
}

const submitForm = async () => {
  isLoading.value = true

  emit('storyGenerationStart')

  abortController.value = new AbortController()

  generateStory(words.value, characterName.value, setting.value, humor.value, abortController.value.signal).then((story) => {
    if (isOpenAIAvailable.value) {
      generateIllustration(story, abortController.value.signal).then((illustration) => {
        emit('storyGenerationComplete', story, illustration)
      })
    } else {
      emit('storyGenerationComplete', story, null)
    }
  }).catch((error) => {
    if (error.name !== 'AbortError') {
      console.error("Error:", error)
      emit('storyGenerationError', error)
    }
  }).finally(() => {
    isLoading.value = false
    abortController.value = null
  })
}

const handleSubmit = () => {
  submitForm()
}

const handleReset = () => {
  words.value = ''
  characterName.value = ''
  setting.value = ''
  humor.value = DEFAULT_HUMOR_VALUE
}

const cancelRequest = () => {
  if (abortController.value) {
    isLoading.value = false
    abortController.value.abort()
  }
}

defineExpose({
  submitForm,
  cancelRequest,
})
</script>