<style scoped lang="postcss">
.story-modal {
  touch-action: none;
}

.story-content {
  -webkit-overflow-scrolling: touch;
}

.ball {
  animation: moveUpDown 1.5s ease-in-out infinite;
}

@keyframes moveUpDown {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-60px);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active {
  transition-delay: 0.5s;
}

.generating-text-enter-active,
.generating-text-leave-active {
  transition: all 0.5s ease;
}

.generating-text-enter-from,
.generating-text-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

:deep(.highlighted-word) {
  /* @apply bg-highlighted-word px-1 rounded; */
  @apply font-bold;
}
</style>

<template>
  <div class="story-modal fixed inset-0 w-full bg-story h-[100dvh]">
    <transition name="fade">
      <div
        v-if="isLoading"
        class="loader-wrapper flex flex-col justify-center items-center h-full w-full overflow-y-hidden"
      >
        <div class="loader flex flex-col items-center">
          <div class="flex justify-center items-center gap-[20px] mb-[80px]">
            <div
              class="ball w-[20px] h-[20px] bg-loading-balls rounded-full relative"
              v-for="n in 3"
              :key="n"
              :style="{ animationDelay: `${(n - 1) * 0.2}s` }"
            ></div>
          </div>
          <div class="h-[40px] relative w-full flex justify-center">
            <!-- Reserve space for text -->
            <transition name="generating-text" mode="out-in">
              <div v-if="showGeneratingText" :key="currentTextIndex" class="text-loading-balls-text text-2xl">
                {{ generatingTexts[currentTextIndex] }}
              </div>
            </transition>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="!isLoading" class="story-content h-full overflow-y-auto pb-[104px]">
        <!-- 
          Here's some logic for handling the fixed image when we have an illustration.
          We're only going to use the fixed image container if we're on mobile. Otherwise,
          we'll just let the image flow as part of the DOM.
        -->
        <div
          v-if="isOpenAIAvailable && illustration"
          :class="[
            'fixed-image-container',
            'fixed top-0 left-0 right-0 z-10 overflow-hidden bg-story',
            'md:static md:bg-transparent md:h-auto',
          ]"
        >
          <div class="p-10 md:px-10 md:py-16 max-w-[700px] mx-auto">
            <!-- This will give us a square ratio for the image on mobile.-->
            <div class="fixed-image-wrapper relative w-full pt-[100%] md:p-0">
              <img
                :class="[
                  'fixed-image',
                  'absolute top-0 left-0 w-full h-full object-cover border border-story-illustration-border rounded-lg',
                  'md:relative md:h-auto',
                ]"
                :src="illustration"
                alt="Illustration"
              />
            </div>
          </div>
        </div>
        <!-- Need to check to see if we've got an illustration, and if we do, we need to make sure the top padding is correct. -->
        <div
          :class="[
            'scrollable-content px-10 pb-10 max-w-[700px] mx-auto',
            'text-[1.375rem] sm:text-2xl leading-relaxed sm:leading-relaxed md:leading-relaxed text-story-text',
            isOpenAIAvailable && illustration
              ? 'pt-[calc(Min(100vw,700px))] md:p-[0px_40px_100px_40px]'
              : 'pt-[40px] md:p[40px_40px_100px_40px]',
          ]"
        >
          <!-- If we get a story back, we're going to highlight the words that are in the word list. -->
          <p v-if="!isError" v-html="highlightedStory"></p>
          <!-- Sometimes we'll get an error message, and we're just displaying it in place of the story. -->
          <p v-else>
            {{ story }}
          </p>
        </div>
      </div>
    </transition>

    <!-- Bottom action buttons -->
    <div class="action-buttons-container fixed bottom-0 left-0 right-0 bg-bottom-bar drop-shadow-bar">
      <div class="flex justify-between items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <FastButton name="Close" type="secondary" @click="emit('closeRequest')">Close</FastButton>
        <FastButton
          :disabled="isLoading"
          :isDisabled="isLoading"
          customClass=""
          @click="$emit('regenerate')"
          name="Regenerate"
        >
          Tell me another story
        </FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, ref, onMounted, onUnmounted, watch, computed } from "vue"
import FastButton from "@/components/FastButton.vue"

const isOpenAIAvailable = inject("isOpenAIAvailable")

const generatingTexts = [
  "Brainstorming plot twists...",
  "Crafting unique characters...",
  "Weaving magical elements...",
  "Designing the story world...",
  "Sprinkling in humor...",
  "Adding suspenseful moments...",
  "Polishing dialogue...",
  "Perfecting the ending...",
  "Enhancing descriptions...",
  "Fine-tuning the narrative...",
  "Conjuring vivid imagery...",
  "Infusing story with emotions...",
  "Developing character arcs...",
  "Adding whimsical details...",
  "Creating memorable scenes...",
  "Sprinkling in vocabulary words...",
  "Polishing the story's rhythm...",
]

const props = defineProps({
  story: {
    type: String,
    required: true,
  },
  illustration: {
    type: String,
    required: false,
  },
  isLoading: {
    type: Boolean,
    required: true,
  },
  wordList: {
    type: Array,
    required: true,
  },
  isError: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const emit = defineEmits(["regenerate", "closeRequest"])

const currentTextIndex = ref(0)
const showGeneratingText = ref(false)
const randomizedGeneratingTexts = ref([])
let textInterval

const clearTextInterval = () => {
  if (textInterval) {
    clearInterval(textInterval)
    textInterval = null
  }
}

const preventScroll = (e) => {
  e.preventDefault()
}

onMounted(() => {
  document.body.style.overflow = "hidden"
  document.addEventListener("touchmove", preventScroll, { passive: false })

  if (props.isLoading) {
    randomizedGeneratingTexts.value = generatingTexts.sort(() => 0.5 - Math.random())
    waitToStartGeneratingText()
    setTimeout(startGeneratingText, 4500)
  }
})

const waitToStartGeneratingText = () => {
  setTimeout(() => {
    showGeneratingText.value = true
  }, 1500)
}

const startGeneratingText = () => {
  showGeneratingText.value = true
  textInterval = setInterval(() => {
    currentTextIndex.value = (currentTextIndex.value + 1) % randomizedGeneratingTexts.value.length
  }, 3000)
}

onUnmounted(() => {
  document.body.style.overflow = ""
  document.removeEventListener("touchmove", preventScroll)
  clearTextInterval()
})

watch(
  () => props.isLoading,
  (newValue) => {
    if (!newValue) {
      clearTextInterval()
      showGeneratingText.value = false
    } else {
      randomizedGeneratingTexts.value = generatingTexts.sort(() => 0.5 - Math.random())
      waitToStartGeneratingText()
      setTimeout(startGeneratingText, 4500)
    }
  },
)

const highlightedStory = computed(() => {
  if (!props.story || !props.wordList.length || props.isError) return props.story

  const escapedWords = props.wordList.map((word) => word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
  const regex = new RegExp(`\\b(${escapedWords.join("|")})\\b`, "gi")

  return props.story.replace(regex, (match) => `<span class="highlighted-word">${match}</span>`)
})
</script>
