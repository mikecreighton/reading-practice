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
      color: #aaa;
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
    border: 1px solid #aaa;
    background-color: #f0f0f0;
    color: #333;
  }

  input.slider {
    display: none;
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

.word-input {
  display: flex;
  margin-top: 12px;

  input {
    flex-grow: 1;
    margin-top: 0;
    margin-right: 10px;
  }

  button {
    height: 60px;
    padding: 0 20px;
    font-size: 18px;
    background-color: #f0f0f0;
    border: 1px solid #aaa;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #e0e0e0;
    }
  }
}

.word-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.chip {
  display: inline-flex;
  align-items: center;
  background-color: #e0e0e0;
  border-radius: 16px;
  padding: 5px 10px;
  font-size: 14px;

  .remove-word {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 18px;
    margin-left: 5px;
    padding: 0 5px;

    &:hover {
      color: #333;
    }
  }
}

.humor-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;

  button {
    font-size: 24px;
    padding: 10px 20px;
    border: 2px solid #aaa;
    background-color: #f0f0f0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background-color: #e0e0e0;
    }

    &.active {
      border-color: #333;
      background-color: #d0d0d0;
    }
  }
}
</style>
<template>
  <form @submit.prevent>
    <label>
      <span class="prevent-wrap">Words to Include in the Story</span>
      <div class="word-input">
        <input
          type="text"
          v-model="newWord"
          @keyup.enter.prevent="addWord"
          placeholder="Enter a word"
        />
        <button type="button" @click="addWord">Add</button>
      </div>
      <div class="word-chips">
        <span v-for="(word, index) in wordList" :key="index" class="chip">
          {{ word }}
          <button @click="removeWord(index)" class="remove-word">&times;</button>
        </span>
      </div>
    </label>
    <label>
      The Story's Main Character
      <input type="text" v-model="characterName" />
    </label>
    <label>
      Where the Story Takes Place
      <input type="text" v-model="setting" />
    </label>
    <label>
      Humor Level
      <div class="humor-buttons">
        <button type="button" @click="setHumor(1)" :class="{ active: humor === 1 }">😐</button>
        <button type="button" @click="setHumor(5)" :class="{ active: humor === 5 }">😊</button>
        <button type="button" @click="setHumor(10)" :class="{ active: humor === 10 }">😂</button>
      </div>
    </label>
    <div class="buttons-container">
      <FastButton
        :disabled="isLoading"
        buttonText="Generate Story"
        @click="handleSubmit"
      ></FastButton>
      <FastButton buttonText="Reset" @click="handleReset"></FastButton>
    </div>
  </form>
</template>

<script setup>
import { ref, inject, computed } from "vue"
import FastButton from "@/components/FastButton.vue"
import { generateStory, generateIllustration } from "@/services/ai"

const DEBUG_STORY_GENERATION = ref(true)
const DEFAULT_HUMOR_VALUE = 3

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
