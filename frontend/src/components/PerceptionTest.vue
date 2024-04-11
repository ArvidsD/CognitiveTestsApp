<script setup>
import { ref } from 'vue';
import TestForm from "@/components/TestForm.vue";
import CanvasImage from "@/components/CanvasImage.vue";
import PerceptionQuestion from "@/components/PerceptionQuestion.vue";
import PerceptionFinish from "@/components/PerceptionFinish.vue";

const isTestFormSubmitted = ref(false);
const isTestCompleted = ref(false); // Jauns stāvokļa mainīgais

function handleTestFormSubmission() {
  isTestFormSubmitted.value = true;
}

// Pievienojiet jaunu funkciju, kas tiks izsaukta, kad tests būs pabeigts
function handleTestCompletion() {
  isTestCompleted.value = true;
}
</script>

<template>
  <div>
    <!-- Parāda TestForm, ja tas vēl nav iesniegts un tests nav pabeigts -->
    <TestForm v-if="!isTestFormSubmitted && !isTestCompleted" @form-submitted="handleTestFormSubmission"/>

    <!-- Parāda CanvasImage un PerceptionQuestion, ja TestForm ir iesniegts, bet tests nav pabeigts -->
    <div v-if="isTestFormSubmitted && !isTestCompleted">
      <CanvasImage/>
      <PerceptionQuestion @test-completed="handleTestCompletion"/>
    </div>

    <!-- Parāda PerceptionFinish, ja tests ir pabeigts -->
    <PerceptionFinish v-if="isTestCompleted"/>
  </div>
</template>

<style scoped>

</style>