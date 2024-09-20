<style scoped style="postcss"></style>

<template>
  <div :class="['App', 'theme-' + settings.theme]">
    <div class="app-content bg-background">
      <InputForm
        ref="inputFormRef"
        :settings="settings"
        :savedInputs="savedInputs"
        @storyGenerationStart="handleStoryGenerationStart"
        @storyGenerationComplete="handleStoryGenerationComplete"
        @storyGenerationError="handleStoryGenerationError"
        @openSettings="handleOpenSettings"
      />

      <div ref="storyModalContainer" class="hidden fixed inset-0 h-full w-full">
        <Transition
          @enter="onStoryModalEnter"
          @leave="onStoryModalLeave"
          @after-leave="onStoryModalAfterLeave"
        >
          <StoryModal
            v-if="isModalOpen"
            :story="story"
            :illustration="illustration"
            :isLoading="isLoading"
            @regenerate="handleRegenerate"
            @closeRequest="handleStoryModalCloseRequest"
          />
        </Transition>
      </div>

      <div ref="settingsModalRef" class="hidden fixed inset-0 h-full w-full">
        <Transition @enter="onSettingsModalEnter" @leave="onSettingsModalLeave">
          <SettingsModal
            v-if="isSettingsModalOpen"
            v-model:settings="settings"
            @save="handleSettingsModalSave"
          />
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted, watch } from "vue"
import StoryModal from "@/views/StoryModal.vue"
import SettingsModal from "@/views/SettingsModal.vue"
import InputForm from "@/views/InputForm.vue"
import { detectOpenAI } from "@/services/ai"
import gsap, { Power4 } from "gsap"

const story = ref(null)
const illustration = ref(null)
const inputFormRef = ref(null)
const isOpenAIAvailable = ref(false)
const isModalOpen = ref(false)
const isLoading = ref(false)
const isSettingsModalOpen = ref(false)
const settings = ref({
  gradeLevel: "2nd",
  theme: "default",
})
const savedInputs = ref({})
const storyModalContainer = ref(null)
const settingsModalRef = ref(null)

const loadSavedInputs = () => {
  const savedInputsData = localStorage.getItem("userInputs")
  if (savedInputsData) {
    savedInputs.value = JSON.parse(savedInputsData)
  }
}

// Call this immediately
loadSavedInputs()

provide("isOpenAIAvailable", isOpenAIAvailable)

onMounted(() => {
  // Load settings from local storage
  const savedSettings = localStorage.getItem("userSettings")
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings)
  }

  detectOpenAI()
    .then((available) => {
      isOpenAIAvailable.value = available
    })
    .catch((error) => {
      // console.error("Error detecting OpenAI availability:", error)
    })
})

watch(isSettingsModalOpen, (isOpen) => {
  if (isOpen) {
    document.body.classList.add("modal-open")
  } else {
    document.body.classList.remove("modal-open")
  }
})

watch(isModalOpen, (isOpen) => {
  if (isOpen) {
    document.body.classList.add("modal-open")
  } else {
    document.body.classList.remove("modal-open")
  }
})

const blurInputs = () => {
  const inputs = document.querySelectorAll("input, textarea")
  inputs.forEach((input) => {
    input.blur()
  })
}

const handleStoryGenerationStart = () => {
  story.value = ""
  isModalOpen.value = true
  isLoading.value = true
  // We need to make sure that none of the inputs are currently focused or we wind up with a weird bug
  blurInputs()
}

const handleStoryGenerationComplete = (generatedStory, generatedIllustration) => {
  story.value = generatedStory
  illustration.value = generatedIllustration
  isLoading.value = false
}

const handleStoryModalCloseRequest = () => {
  isModalOpen.value = false
  isLoading.value = false
}

const onStoryModalEnter = (el, done) => {
  storyModalContainer.value.classList.remove("hidden")

  gsap.from(el, {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeOut,
    onComplete: () => done(),
  })
}

const onStoryModalLeave = (el, done) => {
  inputFormRef.value.cancelRequest()
  gsap.to(el, {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => {
      storyModalContainer.value.classList.add("hidden")
      done()
    },
  })
}

const onStoryModalAfterLeave = () => {
  illustration.value = null
  story.value = null
}

const handleRegenerate = () => {
  inputFormRef.value.cancelRequest()
  illustration.value = null
  inputFormRef.value.submitForm()
}

const handleStoryGenerationError = (error) => {
  illustration.value = null
  isLoading.value = false
  story.value = error.message
}

const handleOpenSettings = () => {
  blurInputs()
  isSettingsModalOpen.value = true
}

const handleSettingsModalSave = () => {
  isSettingsModalOpen.value = false
  localStorage.setItem("userSettings", JSON.stringify(settings.value))
}

const onSettingsModalEnter = (el, done) => {
  settingsModalRef.value.classList.remove("hidden")

  gsap.to(el, {
    duration: 0.5,
    y: "0",
    ease: Power4.easeOut,
    onComplete: () => done(),
  })
}

const onSettingsModalLeave = (el, done) => {
  gsap.to(el, {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => {
      settingsModalRef.value.classList.add("hidden")
      done()
    },
  })
}
</script>
