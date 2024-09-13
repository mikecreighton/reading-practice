<style scoped lang="postcss">
.humor-button {
  @apply flex items-center justify-center text-4xl;
  width: calc((100% - 20px) / 3);
  aspect-ratio: 1 / 1;
}

@screen sm {
  .humor-button {
    @apply w-full h-auto aspect-auto py-3 px-4 flex-row text-2xl justify-center;
  }
}
</style>

<template>
  <form
    @submit.prevent
    class="relative flex flex-col justify-start w-full my-0 mx-auto bg-background min-h-[calc(100vh-104px+40px)] p-10 pb-20 max-w-[700px]"
  >
    <label class="flex flex-col w-full mb-6 md:mb-10 text-lg md:text-2xl text-text">
      
      <span>What words should be included in the story?</span>
      <div class="word-input mt-3 flex w-full">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          @keydown.enter.prevent
          @keyup.space.prevent="addWord"
          @keyup.comma.prevent="addWord"
          placeholder="Enter a word"
          class="flex-1 mr-4 min-w-0 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus placeholder:text-input-placeholder rounded-md"
        />
        <FastButton customClass="flex-shrink-0" @click="addWord">Add</FastButton>
      </div>

      <div class="word-chips flex md:text-lg flex-wrap gap-2 mt-3 md:mt-5">
        <span
          v-for="(word, index) in wordList"
          :key="index"
          class="inline-flex items-center bg-chip rounded-full pt-[6px] pb-1 pl-[14px] pr-3 text-chip-text text-md"
        >
          {{ word }}
          <button @click="removeWord(index)" class="ml-2">
            <i class="bi-x-circle"></i>
          </button>
        </span>
      </div>
    </label>

    <div class="w-full form-character-location-wrap">
      <label class="flex flex-col w-full mb-6 md:mb-10 text-lg md:text-2xl text-text">
        Who's the main character?
        <input
          type="text"
          v-model="characterName"
          class="mt-3 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
        />
      </label>
      <label class="flex flex-col w-full mb-6 md:mb-10 text-lg md:text-2xl text-text">
        Where does the story take place?
        <input
          type="text"
          v-model="setting"
          class="mt-3 py-3 px-4 border border-input-border text-input-text bg-input-background focus:outline-none focus:border-input-border-focus rounded-md"
        />
      </label>
    </div>

    <div class="w-full mb-5 form-humor-wrap">
      <label class="text-lg md:text-2xl text-text mb-3 block">How funny should the story be?</label>
      <div class="humor-buttons flex gap-[10px]">
        <button
          v-for="(item, index) in humorOptions"
          :key="index"
          type="button"
          @click="humor = item.value"
          :class="[
            'humor-button',
            humor === item.value
              ? 'bg-button-secondary-selected border border-button-secondary-selected-border'
              : 'bg-button-secondary border border-button-secondary-border hover:border-button-secondary-hover-border hover:bg-button-secondary-hover',
            'rounded-lg',
          ]"
        >
          <span class="flex items-center justify-center">
            <span>{{ item.emoji }}</span>
            <span class="humor-label hidden sm:inline-block ml-2 mr-1 text-xl text-button-secondary-text">{{ item.label }}</span>
          </span>
        </button>
      </div>
    </div>

    <div
      class="action-buttons-container bg-bottom-bar fixed bottom-0 left-0 right-0 drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <div class="flex items-center">
          <FastButton
            type="secondary"
            customClass="mr-4"
            @click="$emit('openSettings')"
          >
            <i class="bi-gear"></i>
          </FastButton>
          <FastButton
            :disabled="isLoading || (!wordList.length && !characterName && !setting)"
            :isDisabled="isLoading || (!wordList.length && !characterName && !setting)"
            type="secondary"
            @click="handleReset"
          >
            Reset
          </FastButton>
        </div>
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
import { ref, inject, watch, onMounted } from "vue"
import FastButton from "@/components/FastButton.vue"
import { generateStory, generateIllustration } from "@/services/ai"

const DEBUG_INPUT_FORM = ref(false)
const DEBUG_STORY_GENERATION = ref(false)

const newWord = ref("")
const wordList = ref([])

const addWord = () => {
  if (newWord.value.trim()) {
    wordList.value.push(newWord.value.trim().toLowerCase())
    newWord.value = ""
  }
}

const removeWord = (index) => {
  wordList.value.splice(index, 1)
}

const characterName = ref("")
const setting = ref("")
const humor = ref(5)
const isLoading = ref(false)
const abortController = ref(null)
const isOpenAIAvailable = inject("isOpenAIAvailable")

const props = defineProps({
  settings: {
    type: Object,
    required: true
  },
  savedInputs: {
    type: Object,
    required: false,
    default: () => ({})
  }
})

const emit = defineEmits([
  "storyGenerationStart",
  "storyGenerationComplete",
  "storyGenerationError",
  "openSettings",
])

const loadSavedInputs = () => {
  if (!DEBUG_INPUT_FORM.value) {
    wordList.value = props.savedInputs.wordList || []
    characterName.value = props.savedInputs.characterName || ""
    setting.value = props.savedInputs.setting || ""
    humor.value = props.savedInputs.humor || 5
  } else {
    // Set debug values
    wordList.value = ["collaborate", "decipher", "empathy", "hypothesis", "innovative"]
    characterName.value = "A scientist"
    setting.value = "A school bus"
    humor.value = 10
  }
}

// Watch for changes in savedInputs prop
watch(() => props.savedInputs, (newSavedInputs) => {
  if (Object.keys(newSavedInputs).length > 0) {
    loadSavedInputs()
  }
}, { immediate: true, deep: true })

onMounted(() => {
  loadSavedInputs()
})

// Watch for changes in input values and save to local storage
watch([wordList, characterName, setting, humor], () => {
  const inputValues = {
    wordList: wordList.value,
    characterName: characterName.value,
    setting: setting.value,
    humor: humor.value
  }
  console.log("InputForm Watch", inputValues)
  localStorage.setItem('userInputs', JSON.stringify(inputValues))
}, { deep: true })

const submitForm = async () => {
  isLoading.value = true

  // Make sure all the words are lowercase
  wordList.value = wordList.value.map((word) => word.toLowerCase())

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
    props.settings.gradeLevel,
    abortController.value.signal,
  )
    .then((story) => {
      if (isOpenAIAvailable.value) {
        abortController.value = new AbortController()
        generateIllustration(story, props.settings.gradeLevel, abortController.value.signal).then((illustration) => {
          emit("storyGenerationComplete", story, illustration)
        })
      } else {
        emit("storyGenerationComplete", story, null)
      }
    })
    .catch((error) => {
      if (error.name !== "AbortError") {
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
  humor.value = 5
}

const cancelRequest = () => {
  if (abortController.value) {
    isLoading.value = false
    abortController.value.abort()
  }
}

const humorOptions = [
  { value: 1, emoji: "😐", label: "Not funny" },
  { value: 5, emoji: "😊", label: "Funny" },
  { value: 10, emoji: "😂", label: "OMGLOL" },
]

defineExpose({
  submitForm,
  cancelRequest,
})
</script>
