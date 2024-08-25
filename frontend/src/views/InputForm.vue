<template>
  <form
    @submit.prevent
    class="relative flex flex-col justify-start w-full my-0 mx-auto bg-white max-w-[700px] p-10 min-h-[calc(100vh-104px+40px)] pb-20"
  >
    <label class="flex flex-col w-full mb-6 text-lg text-gray-800">
      <span class="whitespace-nowrap">What words should be included in the story?</span>
      <div class="word-input mt-3 flex w-full">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          @keydown.enter.prevent
          placeholder="Enter a word"
          class="flex-1 mr-4 min-w-0 py-3 px-4 border border-gray-300 rounded-md"
        />
        <FastButton
          customClass="flex-shrink-0 border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white"
          @click="addWord"
        >
          Add
        </FastButton>
      </div>
      <div class="word-chips flex flex-wrap gap-2 mt-3">
        <span
          v-for="(word, index) in wordList"
          :key="index"
          class="inline-flex items-center bg-gray-200 rounded-full py-1 px-3 text-sm"
        >
          {{ word }}
          <button @click="removeWord(index)" class="ml-1 text-gray-600 hover:text-gray-800">
            <i class="bi-x-circle"></i>
          </button>
        </span>
      </div>
    </label>
    <div class="w-full form-character-location-wrap">
      <label class="flex flex-col w-full mb-6 text-lg text-gray-800">
        Who's the main character?
        <input
          type="text"
          v-model="characterName"
          class="mt-3 py-3 px-4 border border-gray-300 rounded-md"
        />
      </label>
      <label class="flex flex-col w-full mb-6 text-lg text-gray-800">
        Where does the story take place?
        <input
          type="text"
          v-model="setting"
          class="mt-3 py-3 px-4 border border-gray-300 rounded-md"
        />
      </label>
    </div>
    <div class="w-full mb-5 form-humor-wrap">
      <label class="mb-3 text-lg text-gray-800">How funny should the story be?</label>
      <div class="humor-buttons flex justify-between">
        <button
          type="button"
          @click="setHumor(1)"
          :class="{
            'bg-blue-500 text-white': humor === 1,
            'border border-blue-500 text-blue-500': humor !== 1,
            'py-2 px-4 rounded-lg text-2xl': true,
          }"
        >
          😐
        </button>
        <button
          type="button"
          @click="setHumor(5)"
          :class="{
            'bg-blue-500 text-white': humor === 5,
            'border border-blue-500 text-blue-500': humor !== 5,
            'py-2 px-4 rounded-lg text-2xl': true,
          }"
        >
          😊
        </button>
        <button
          type="button"
          @click="setHumor(10)"
          :class="{
            'bg-blue-500 text-white': humor === 10,
            'border border-blue-500 text-blue-500': humor !== 10,
            'py-2 px-4 rounded-lg text-2xl': true,
          }"
        >
          😂
        </button>
      </div>
    </div>
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 h-[104px] p-5 bg-white shadow-md"
    >
      <div class="flex justify-between items-center max-w-[700px] mx-auto my-0">
        <FastButton
          :disabled="isLoading || (!wordList.length && !characterName && !setting)"
          customClass="bg-gray-500 text-white py-2 px-4 rounded-lg text-lg"
          @click="handleReset"
        >
          Reset
        </FastButton>
        <FastButton
          :disabled="isLoading || !wordList.length || !characterName || !setting"
          customClass="bg-blue-500 text-white py-2 px-4 rounded-lg text-lg"
          @click="handleSubmit"
        >
          Generate Story
        </FastButton>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, inject } from "vue"
import FastButton from "@/components/FastButton.vue"
import { generateStory, generateIllustration } from "@/services/ai"

const DEBUG_STORY_GENERATION = ref(false)
const DEFAULT_HUMOR_VALUE = 5

const newWord = ref("")
const wordList = ref([])

const addWord = () => {
  if (newWord.value.trim()) {
    wordList.value.push(newWord.value.trim())
    newWord.value = ""
  }
}

const removeWord = (index) => {
  wordList.value.splice(index, 1)
}

const characterName = ref("")
const setting = ref("")
const humor = ref(DEFAULT_HUMOR_VALUE)
const isLoading = ref(false)
const abortController = ref(null)
const isOpenAIAvailable = inject("isOpenAIAvailable")

const emit = defineEmits([
  "storyGenerationStart",
  "storyGenerationComplete",
  "storyGenerationError",
])

if (DEBUG_STORY_GENERATION.value) {
  wordList.value = ["friend", "because", "weather", "bicycle", "favorite"]
  characterName.value = "The Big Bad Wolf"
  setting.value = "A school bus"
  humor.value = 10
}

const setHumor = (value) => {
  humor.value = value
}

const submitForm = async () => {
  isLoading.value = true

  emit("storyGenerationStart")

  abortController.value = new AbortController()

  const words = wordList.value.join(",")

  generateStory(
    words,
    characterName.value,
    setting.value,
    humor.value,
    abortController.value.signal,
  )
    .then((story) => {
      if (isOpenAIAvailable.value) {
        generateIllustration(story, abortController.value.signal).then((illustration) => {
          emit("storyGenerationComplete", story, illustration)
        })
      } else {
        emit("storyGenerationComplete", story, null)
      }
    })
    .catch((error) => {
      if (error.name !== "AbortError") {
        console.error("Error:", error)
        emit("storyGenerationError", error)
      }
    })
    .finally(() => {
      isLoading.value = false
      abortController.value = null
    })
}

const handleSubmit = () => {
  submitForm()
}

const handleReset = () => {
  wordList.value = []
  newWord.value = ""
  characterName.value = ""
  setting.value = ""
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

<style lang="scss" scoped>
// Remove all styles here, as they're now handled by Tailwind classes
</style>
