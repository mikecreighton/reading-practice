<style scoped></style>

<template>
  <form
    @submit.prevent
    class="relative flex flex-col justify-start w-full my-0 mx-auto bg-white max-w-[700px] min-h-[calc(100vh-104px+40px)] p-10 pb-20"
  >
    <label class="flex flex-col w-full mb-6 text-lg text-gray-800">
      <span>What words should be included in the story?</span>
      <div class="word-input mt-3 flex w-full">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          @keydown.enter.prevent
          placeholder="Enter a word"
          class="flex-1 mr-4 min-w-0 py-3 px-4 border border-input-border bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
        />
        <FastButton customClass="flex-shrink-0" @click="addWord">Add</FastButton>
      </div>
      <div class="word-chips flex flex-wrap gap-2 mt-3">
        <span
          v-for="(word, index) in wordList"
          :key="index"
          class="inline-flex items-center bg-gray-200 rounded-full pt-[6px] pb-1 pl-[14px] pr-3 text-md"
        >
          {{ word }}
          <button @click="removeWord(index)" class="ml-2 text-gray-600 hover:text-gray-800">
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
          class="mt-3 py-3 px-4 border border-input-border bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
        />
      </label>
      <label class="flex flex-col w-full mb-6 text-lg text-gray-800">
        Where does the story take place?
        <input
          type="text"
          v-model="setting"
          class="mt-3 py-3 px-4 border border-input-border bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
        />
      </label>
    </div>
    <div class="w-full mb-5 form-humor-wrap">
      <label class="text-lg text-gray-800 mb-3 block">How funny should the story be?</label>
      <div class="humor-buttons flex justify-between">
        <button
          v-for="i in [1, 5, 10]"
          :key="i"
          type="button"
          @click="setHumor(i)"
          :class="{
            'bg-input-background border border-input-border-focus': humor === i,
            'bg-white border border-input-border': humor !== i,
            'py-3 px-4 rounded-lg text-2xl': true,
          }"
        >
          {{ i == 1 ? "😐" : i == 5 ? "😊" : "😂" }}
        </button>
      </div>
    </div>
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 px-10 py-5 bg-white drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] mx-auto my-0">
        <FastButton
          :disabled="isLoading || (!wordList.length && !characterName && !setting)"
          :isDisabled="isLoading || (!wordList.length && !characterName && !setting)"
          type="secondary"
          @click="handleReset"
        >
          Reset
        </FastButton>
        <FastButton
          :disabled="isLoading || !wordList.length || !characterName || !setting"
          :isDisabled="isLoading || !wordList.length || !characterName || !setting"
          customClass=""
          @click="handleSubmit"
        >
          Go!
        </FastButton>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, inject } from "vue"
import FastButton from "@/components/FastButton.vue"
import { generateStory, generateIllustration } from "@/services/ai"

const DEBUG_INPUT_FORM = ref(true)
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

if (DEBUG_INPUT_FORM.value) {
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

  if (DEBUG_STORY_GENERATION.value) {
    const tempStory = `The Big Bad Wolf hopped on the school bus, carrying his favorite bicycle. His friend, a little pig, asked, "Why did you bring that?" The wolf replied, "Because the weather is nice for riding!" Suddenly, the bus driver hit a bump, and the wolf's bicycle bounced around. It knocked over lunch boxes and backpacks. The bicycle wheels spun wildly, spraying mud everywhere. All the kids on the bus got splattered, and their hair stood up like crazy mohawks. The wolf looked at the mess and said, "Oops! I guess bikes don't belong on buses!" The Big Bad Wolf hopped on the school bus, carrying his favorite bicycle. His friend, a little pig, asked, "Why did you bring that?" The wolf replied, "Because the weather is nice for riding!" Suddenly, the bus driver hit a bump, and the wolf's bicycle bounced around. It knocked over lunch boxes and backpacks. The bicycle wheels spun wildly, spraying mud everywhere. All the kids on the bus got splattered, and their hair stood up like crazy mohawks. The wolf looked at the mess and said, "Oops! I guess bikes don't belong on buses!"`
    emit("storyGenerationComplete", tempStory, "https://placehold.co/600x400")
    isLoading.value = false
    return
  }

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
