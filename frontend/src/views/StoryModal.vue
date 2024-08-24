<style lang="scss" scoped>
.story-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #fff;
  overflow-y: scroll;
  transform: translateY(100%);

  .story-modal-content {
    padding: 100px 20px 80px 20px;
    width: 100%;

    p {
      font-size: 20px;
      line-height: 1.8;
    }

    @media (min-width: 768px) {
      padding: 60px 40px 100px 40px;
      p {
        font-size: 30px;
        line-height: 1.6;
      }
    }

    @media (min-width: 1200px) {
      p {
        font-size: 36px;
      }
    }
  }

  .story-modal-close-button {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 30px;
    width: 60px;
    height: 60px;
    cursor: pointer;
    user-select: none;
    border: none;
    color: #fff;
    text-align: center;
    background-color: #101010;
    border-radius: 12px;
    transition: background-color 0.1s ease-in-out;
    padding: 0;

    &:hover,
    &:focus,
    &:active {
      background-color: #303030;
    }
  }
}
</style>
<template>
  <div class="story-modal">
    <div class="story-modal-content d-flex flex-column justify-content-center align-items-center">
      <img
        width="100%"
        class="mb-4"
        v-if="isOpenAIAvailable && illustration"
        :src="illustration"
        alt="Illustration"
      />
      <p>{{ story }}</p>
      <FastButton customClass="story-modal-close-button" @click="emit('closeRequest')">&#x2715;</FastButton>
      <FastButton
        customClass="regenerate-button"
        @click="$emit('regenerate')"
      >Regenerate</FastButton>
    </div>
  </div>
</template>

<script setup>
import { inject } from "vue"
import FastButton from "@/components/FastButton.vue"

const isOpenAIAvailable = inject("isOpenAIAvailable")

const props = defineProps({
  story: {
    type: String,
    required: true,
  },
  illustration: {
    type: String,
    required: false,
  },
})

const emit = defineEmits(["regenerate", "closeRequest"])
</script>
