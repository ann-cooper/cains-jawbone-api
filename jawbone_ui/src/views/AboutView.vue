<script setup>
import WelcomeItem from '../components/WelcomeItem.vue'
import DocumentationIcon from '../components/icons/IconDocumentation.vue'
</script>

<template>
  <main>
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>Cain's Jawbone, Torquemada, 1934</template>
    <li>From <a href="https://en.wikipedia.org/wiki/Cain%27s_Jawbone" target="_blank" rel="noopener">wikipedia</a></li>
    <li>The Guardian, on <a href="https://www.theguardian.com/books/2020/nov/10/literary-puzzle-solved-for-just-third-time-in-almost-100-years-cains-jawbone" target="_blank" rel="noopener">solving</a> the puzzle</li>
  </WelcomeItem>
</main>
</template>