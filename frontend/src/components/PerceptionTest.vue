<script setup>
import {ref} from 'vue';
import TestForm from "@/components/TestForm.vue";
import CanvasImage from "@/components/CanvasImage.vue";
import PerceptionQuestion from "@/components/PerceptionQuestion.vue";
import {onMounted} from 'vue';
import DemographicQuestions from "@/components/DemographicQuestions.vue";

const isTestFormSubmitted = ref(false);
const isTestCompleted = ref(false);

function handleTestFormSubmission() {
  isTestFormSubmitted.value = true;
  sessionStorage.setItem('isTestFormSubmitted', 'true');
}

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

  const lastAnsweredQuestionId = sessionStorage.getItem('lastAnsweredQuestionId') || null;
  if (lastAnsweredQuestionId && !isTestCompleted.value) {

  }
});
</script>

<template>
  <div class="container mt-5 custom-container">

    <TestForm v-if="!isTestFormSubmitted && !isTestCompleted" @form-submitted="handleTestFormSubmission"/>

    <div v-if="isTestFormSubmitted && !isTestCompleted">
      <CanvasImage class="row justify-content-center"/>
      <PerceptionQuestion @test-completed="handleTestCompletion" class="mb-5"/>
    </div>

    <DemographicQuestions v-if="isTestCompleted"/>
  </div>
</template>

<style scoped>
.custom-container {
  max-width: 800px;
  margin: 0 auto;
}
</style>