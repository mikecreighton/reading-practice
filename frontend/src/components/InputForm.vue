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
  <form @submit.prevent="handleSubmit">
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
      <button class="button-labeled" type="submit" :disabled="isLoading">
        Generate Story
      </button>
      <button class="button-labeled" type="reset" @click="handleReset">
        Reset
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const words = ref('');
const characterName = ref('');
const setting = ref('');
const humor = ref(3);
const isLoading = ref(false);
const abortController = ref(null);

const emit = defineEmits(['storyPartReceived']);

const submitForm = async () => {
  isLoading.value = true;
  abortController.value = new AbortController();

  let baseURL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : "";

  try {
    const response = await fetch(baseURL + "/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        words: words.value,
        subject: characterName.value,
        setting: setting.value,
        humor: humor.value + "",
      }),
      signal: abortController.value.signal,
    });

    if (!response.ok) {
      throw new Error(`HTTP error status: ${response.statusText}`);
    } else {
      const reader = response.body.getReader();
      let story = "";
      let chunk;

      while ((chunk = await reader.read()) && !chunk.done) {
        story += new TextDecoder("utf-8").decode(chunk.value);
        emit('storyPartReceived', story);
      }
    }
  } catch (error) {
    if (error.name === "AbortError") {
      console.log("Fetch request cancelled");
    } else {
      console.error("Error:", error);
    }
  } finally {
    isLoading.value = false;
  }
};

const cancelRequest = () => {
  if (abortController.value) {
    abortController.value.abort();
  }
};

const handleSubmit = () => {
  submitForm();
};

const handleReset = () => {
  words.value = '';
  characterName.value = '';
  setting.value = '';
  humor.value = 3;
};

defineExpose({
  submitForm,
  cancelRequest,
});
</script>