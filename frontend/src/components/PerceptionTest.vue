<script setup>
import { ref } from 'vue';
import TestForm from "@/components/TestForm.vue";
import CanvasImage from "@/components/CanvasImage.vue";
import PerceptionQuestion from "@/components/PerceptionQuestion.vue";
import PerceptionFinish from "@/components/PerceptionFinish.vue";
import { onMounted } from 'vue';
import DemographicQuestions from "@/components/DemographicQuestions.vue";
const isTestFormSubmitted = ref(false);
const isTestCompleted = ref(false); // Jauns stāvokļa mainīgais

function handleTestFormSubmission() {
  isTestFormSubmitted.value = true;
  sessionStorage.setItem('isTestFormSubmitted', 'true');
}

// Pievienojiet jaunu funkciju, kas tiks izsaukta, kad tests būs pabeigts
function handleTestCompletion() {
  isTestCompleted.value = true;
  sessionStorage.setItem('isTestCompleted', 'true');
}
onMounted(() => {
  if (sessionStorage.getItem('isTestFormSubmitted') === 'true') {
    isTestFormSubmitted.value = true;
  }
  if (sessionStorage.getItem('isTestCompleted') === 'true') {
    isTestCompleted.value = true;
  }
  // Ja ir saglabāts pēdējais atbildētais jautājuma ID, ielādējiet attiecīgo jautājumu
  const lastAnsweredQuestionId = sessionStorage.getItem('lastAnsweredQuestionId') || null;
  if (lastAnsweredQuestionId && !isTestCompleted.value) {
    // Funkcija, kas ielādē jautājumu, izmantojot lastAnsweredQuestionId
  }
});
</script>

<template>
  <div class="container mt-5 custom-container">
    <!-- Parāda TestForm, ja tas vēl nav iesniegts un tests nav pabeigts -->
    <TestForm v-if="!isTestFormSubmitted && !isTestCompleted" @form-submitted="handleTestFormSubmission"/>

    <!-- Parāda CanvasImage un PerceptionQuestion, ja TestForm ir iesniegts, bet tests nav pabeigts -->
    <div v-if="isTestFormSubmitted && !isTestCompleted">
      <CanvasImage class="mb-5"/>
      <PerceptionQuestion @test-completed="handleTestCompletion" class="mb-5"/>
    </div>

    <!-- Parāda PerceptionFinish, ja tests ir pabeigts -->
    <DemographicQuestions v-if="isTestCompleted"/>
  </div>
</template>

<style scoped>
.custom-container {
  max-width: 800px; /* Norāda maksimālo platumu */
  margin: 0 auto; /* Centrē saturu horizontāli */
}
</style>