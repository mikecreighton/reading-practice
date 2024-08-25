<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

$form-padding: 40px;
$action-buttons-height: 104px;
$form-max-width: 700px;

form {
  background-color: #fff;
  max-width: $form-max-width;
  padding: $form-padding;
  min-height: calc(100vh - ($action-buttons-height) + $form-padding);
  padding-bottom: $form-padding * 2;

  label {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 24px;
    font-size: 1.2rem;
    color: #333;

    .helper {
      color: #aaa;
      display: inline;
      font-size: 80%;
    }
  }

  // make the buttons sit side-by-side
  .action-buttons-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    gap: 8px;
    height: $action-buttons-height;
    padding: 20px $form-padding;
    background-color: #fff;
    box-shadow: 0 -2px 12px -1px rgba(0, 0, 0, 0.1);

    div {
      max-width: $form-max-width;
    }
  }
}

.word-input {
  display: flex;
  width: 100%;

  input {
    flex: 1;
    margin-top: 0;
    margin-right: 16px;
    min-width: 0;
  }
}

.chip {
  display: inline-flex;
  align-items: center;
  background-color: #e0e0e0;
  border-radius: 17px;
  padding: 5px 8px 5px 15px;
  font-size: 14px;
  line-height: 24px;

  .remove-word {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 18px;
    margin-left: 5px;
    padding: 0 5px;
    display: flex;
    align-items: center;

    &:hover {
      color: #333;
    }
  }
}

.humor-buttons {
  display: flex;
  justify-content: space-between;
}
</style>
<template>
  <form
    @submit.prevent
    class="position-relative d-flex flex-column justify-content-start w-100 my-0 mx-auto"
  >
    <label>
      <span class="prevent-wrap">What words should be included in the story?</span>
      <div class="word-input mt-3">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          @keydown.enter.prevent
          placeholder="Enter a word"
          class="form-control py-3"
        />
        <FastButton customClass="flex-shrink-0 btn-outline-primary" @click="addWord">
          Add
        </FastButton>
      </div>
      <div class="word-chips d-flex flex-wrap gap-2 mt-3">
        <span v-for="(word, index) in wordList" :key="index" class="chip">
          {{ word }}
          <button @click="removeWord(index)" class="remove-word">
            <i class="bi-x-circle"></i>
          </button>
        </span>
      </div>
    </label>
    <div class="w-100 form-character-location-wrap">
      <label>
        Who's the main character?
        <input type="text" v-model="characterName" class="form-control mt-3 py-3" />
      </label>
      <label>
        Where does the story take place?
        <input type="text" v-model="setting" class="form-control mt-3 py-3" />
      </label>
    </div>
    <div class="w-100 mb-5 form-humor-wrap">
      <label class="mb-3">How funny should the story be?</label>
      <div class="humor-buttons">
        <button
          type="button"
          @click="setHumor(1)"
          :class="{ active: humor === 1, 'btn-outline-primary': true, btn: true, 'btn-lg': true }"
        >
          😐
        </button>
        <button
          type="button"
          @click="setHumor(5)"
          :class="{ active: humor === 5, 'btn-outline-primary': true, btn: true, 'btn-lg': true }"
        >
          😊
        </button>
        <button
          type="button"
          @click="setHumor(10)"
          :class="{ active: humor === 10, 'btn-outline-primary': true, btn: true, 'btn-lg': true }"
        >
          😂
        </button>
      </div>
    </div>
    <div class="action-buttons-container w-100">
      <div class="d-flex justify-content-between align-items-center mx-auto my-0">
        <FastButton
          :disabled="isLoading || (!wordList.length && !characterName && !setting)"
          customClass="btn-secondary btn-lg"
          @click="handleReset"
        >
          Reset
        </FastButton>
        <FastButton
          :disabled="isLoading || !wordList.length || !characterName || !setting"
          customClass="btn-primary btn-lg"
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
