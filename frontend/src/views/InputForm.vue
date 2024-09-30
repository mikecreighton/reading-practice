<style scoped lang="postcss"></style>

<template>
  <form
    @submit.prevent
    class="relative flex flex-col justify-start w-full my-0 mx-auto bg-background min-h-[calc(100dvh-104px+40px)] p-10 pb-24 max-w-[700px]"
    :class="{ 'no-scroll': preventScroll }"
  >
    <div class="mb-6 md:mb-10">
      <label class="block text-lg md:text-2xl text-text mb-3 md:mb-4" for="grade-level">Grade Level</label>
      <div class="relative">
        <select
          id="grade-level"
          v-model="settings.gradeLevel"
          class="w-full py-3 px-4 md:text-2xl border-2 border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus rounded-lg appearance-none"
        >
          <option v-for="grade in gradeOptions" :key="grade" :value="grade">{{ grade }}</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-input-text">
          <i class="bi-chevron-down absolute right-4 top-4 md:top-5"></i>
        </div>
      </div>
    </div>
    <label class="flex flex-col w-full mb-8 md:mb-10 text-lg md:text-2xl text-text">
      <span>Enter the words to appear in your story:</span>
      <div class="word-input mt-3 flex w-full">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          @keydown.enter.prevent
          @keydown.space.prevent="addWord"
          @keydown="handleKeyDown"
          :disabled="wordList.length >= MAX_WORDS"
          :placeholder="wordList.length >= MAX_WORDS ? 'Sorry, 10 words maximum.' : 'Enter a word'"
          class="flex-1 mr-4 min-w-0 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus focus:bg-input-background-focus placeholder:text-input-placeholder rounded-lg"
          :class="{ 'opacity-75 cursor-not-allowed': wordList.length >= MAX_WORDS }"
        />
        <FastButton
          customClass="flex-shrink-0"
          @click="addWord"
          :disabled="wordList.length >= MAX_WORDS"
          :isDisabled="wordList.length >= MAX_WORDS"
        >
          Add
        </FastButton>
      </div>

      <div v-if="wordList.length" class="word-chips flex md:text-lg mt-3 md:mt-5 flex-wrap gap-2">
        <span
          v-for="(word, index) in wordList"
          :key="index"
          class="inline-flex items-center bg-chip rounded-full pt-[6px] pb-1 pl-[14px] pr-3 text-chip-text text-md"
        >
          <span class="relative top-[-1px]">{{ word }}</span>
          <button @click="removeWord(index)" class="ml-2 relative top-[1px]">
            <i class="bi-x-circle"></i>
          </button>
        </span>
      </div>
    </label>

    <div class="w-full form-character-location-wrap">
      <label class="flex flex-col w-full mb-8 md:mb-10 text-lg md:text-2xl text-text">
        Who's the main character?
        <input
          type="text"
          v-model="characterName"
          class="mt-3 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus focus:bg-input-background-focus rounded-lg"
        />
      </label>
      <label class="flex flex-col w-full mb-8 md:mb-10 text-lg md:text-2xl text-text">
        Where should your story take place?
        <input
          type="text"
          v-model="setting"
          class="mt-3 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus focus:bg-input-background-focus rounded-lg"
        />
      </label>
    </div>

    <div class="w-full mb-5 form-humor-wrap">
      <label class="text-lg md:text-2xl text-text mb-3 block">How funny should your story be?</label>
      <div class="humor-buttons flex gap-[10px]">
        <button
          v-for="(item, index) in humorOptions"
          :key="index"
          type="button"
          @click="humor = item.value"
          :class="[
            'humor-button',
            'flex items-center justify-center text-4xl rounded-lg aspect-square w-[calc((100%-20px)/3)]',
            'sm:w-full sm:h-auto sm:aspect-auto sm:py-3 sm:px-4 sm:flex-row sm:text-2xl sm:justify-center',
            humor === item.value
              ? 'bg-button-option-selected border-2 border-button-option-selected-border'
              : 'bg-button-option border-2 border-button-option-border hover:border-button-option-hover-border hover:bg-button-option-hover',
          ]"
        >
          <span class="flex items-center justify-center">
            <span>{{ item.emoji }}</span>
            <span class="humor-label hidden sm:inline-block ml-2 mr-1 text-xl text-button-secondary-text">
              {{ item.label }}
            </span>
          </span>
        </button>
      </div>
    </div>

    <div class="action-buttons-container bg-bottom-bar fixed bottom-0 left-0 right-0 drop-shadow-bar">
      <div class="flex justify-between items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <div class="flex items-center">
          <FastButton type="secondary" customClass="mr-4" @click="$emit('openSettings')" name="Settings">
            <i class="bi-gear"></i>
          </FastButton>
          <FastButton
            :disabled="isLoading || (!wordList.length && !characterName && !setting && !humor)"
            :isDisabled="isLoading || (!wordList.length && !characterName && !setting && !humor)"
            type="secondary"
            @click="handleReset"
            name="Reset"
          >
            Reset
          </FastButton>
        </div>
        <FastButton
          :disabled="isLoading || !wordList.length || !characterName || !setting || !humor"
          :isDisabled="isLoading || !wordList.length || !characterName || !setting || !humor"
          customClass=""
          @click="handleSubmit"
          name="Go"
        >
          Go!
        </FastButton>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, inject, watch, onMounted, defineModel } from "vue"
import FastButton from "@/components/FastButton.vue"
import { generateStory, generateIllustration } from "@/services/ai"
import { LOCAL_STORAGE_INPUTS_KEY } from "@/settings-constants"
import { debugWordList, debugCharacterName, debugSetting, debugHumor, debugStoryContent } from "@/debug-values"

const props = defineProps({
  savedInputs: {
    type: Object,
    required: false,
    default: () => ({}),
  },
  preventScroll: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const emit = defineEmits(["storyGenerationStart", "storyGenerationComplete", "storyGenerationError", "openSettings"])

const DEBUG_INPUT_FORM = ref(import.meta.env.VITE_DEBUG_INPUT_FORM === "true")
const DEBUG_STORY_GENERATION = ref(import.meta.env.VITE_DEBUG_STORY_GENERATION === "true")

const newWord = ref("")
const wordList = ref([])
const characterName = ref("")
const setting = ref("")
const humor = ref(null)
const isLoading = ref(false)
const abortController = ref(null)
const illustrationAbortController = ref(null)
const isOpenAIAvailable = inject("isOpenAIAvailable")
const MAX_WORDS = ref(10)
const gradeOptions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
const settings = defineModel("settings")

onMounted(() => {
  if (!DEBUG_INPUT_FORM.value) {
    wordList.value = props.savedInputs.wordList || []
    characterName.value = props.savedInputs.characterName || ""
    setting.value = props.savedInputs.setting || ""
    humor.value = props.savedInputs.humor || null
  } else {
    // Set debug values
    wordList.value = [...debugWordList]
    characterName.value = debugCharacterName
    setting.value = debugSetting
    humor.value = debugHumor
  }
})

// Watch for changes in input values and save to local storage
watch(
  [wordList, characterName, setting, humor],
  () => {
    const inputValues = {
      wordList: wordList.value,
      characterName: characterName.value,
      setting: setting.value,
      humor: humor.value,
    }
    localStorage.setItem(LOCAL_STORAGE_INPUTS_KEY, JSON.stringify(inputValues))
  },
  { deep: true },
)

const handleKeyDown = (event) => {
  // We have to do this because @keydown.comma.prevent isn't firing for some reason.
  // :v-on:keydown., and :v-on:keydown.,.prevent don't work either.
  // Reference this to see what _should_ work: https://v3-migration.vuejs.org/breaking-changes/keycode-modifiers#migration-strategy
  // I don't see `comma` in the list of key aliases here: https://vuejs.org/guide/essentials/event-handling.html#key-modifiers
  // So, I'm going to assume that this is the only way to do it.
  if (event.key === "," || event.keyCode === 188) {
    event.preventDefault()
    addWord()
  }
}

const addWord = () => {
  if (newWord.value.trim() && wordList.value.length < MAX_WORDS.value) {
    const word = newWord.value
      .trim()
      .toLowerCase()
      .replace(/[^\w\s]/gi, "")
    wordList.value.push(word)
    newWord.value = ""
  }
}

const removeWord = (index) => {
  wordList.value.splice(index, 1)
}

const submitForm = async () => {
  isLoading.value = true

  // Make sure all the words are lowercase
  wordList.value = wordList.value.map((word) => word.toLowerCase())

  emit("storyGenerationStart", wordList.value)

  if (DEBUG_STORY_GENERATION.value) {
    const tempStory = debugStoryContent
    emit(
      "storyGenerationComplete",
      tempStory,
      window.innerWidth > 768 ? "https://placehold.co/600x400" : "https://placehold.co/600x600",
    )
    isLoading.value = false
    return
  }

  abortController.value = new AbortController()

  const words = wordList.value.join(", ")

  generateStory(
    words,
    characterName.value,
    setting.value,
    humor.value,
    props.settings.gradeLevel,
    abortController.value.signal,
  )
    .then((story) => {
      if (isOpenAIAvailable.value) {
        illustrationAbortController.value = new AbortController()
        return generateIllustration(story, props.settings.gradeLevel, illustrationAbortController.value.signal).then(
          (illustration) => {
            return { story, illustration }
          },
        )
      } else {
        return { story, illustration: null }
      }
    })
    .then(({ story, illustration }) => {
      emit("storyGenerationComplete", story, illustration)
    })
    .catch((error) => {
      console.warn("Error generating story or illustration", error)
      if (error.name !== "AbortError") {
        emit("storyGenerationError", error)
      }
    })
    .finally(() => {
      isLoading.value = false
      abortController.value = null
      illustrationAbortController.value = null
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
  humor.value = null
}

const cancelRequest = () => {
  if (abortController.value) {
    isLoading.value = false
    abortController.value.abort()
  }
  if (illustrationAbortController.value) {
    isLoading.value = false
    illustrationAbortController.value.abort()
  }
}

const humorOptions = [
  { value: 1, emoji: "😐", label: "Not funny" },
  { value: 5, emoji: "😊", label: "A little funny" },
  { value: 10, emoji: "😂", label: "LOL" },
]

defineExpose({
  submitForm,
  cancelRequest,
})
</script>
