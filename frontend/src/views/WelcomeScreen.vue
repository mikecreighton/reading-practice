<template>
  <div class="h-screen bg-background text-text">
    <div class="flex flex-col items-center justify-center px-4 max-w-[700px] mx-auto h-full">
      <h1 class="text-4xl md:text-6xl font-bold mb-4">Reading Practice</h1>
      <p class="text-lg md:text-2xl mb-8 text-center">
        Welcome to our Reading Practice app! Enhance your reading and spelling skills with custom-generated stories tailored for young learners.
      </p>
      <div class="flex space-x-4 mb-8">
        <a href="https://github.com/your-repo" target="_blank" class="text-primary hover:underline">GitHub Repo</a>
        <a href="https://twitter.com/mikecreighton" target="_blank" class="text-primary hover:underline">@mikecreighton</a>
      </div>
      <FastButton type="primary" @click="$emit('getStarted')">Get Started</FastButton>
    </div>
  </div>
</template>

<script setup>
import FastButton from "@/components/FastButton.vue"
</script>