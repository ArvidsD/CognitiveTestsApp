<template>
  <div class="container mt-2 custom-container mx-auto">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <p v-if="question">Iedomājies, ka esi <strong>{{ question.object1.name }}</strong> un skaties uz
          <strong>{{ question.object2.name }}</strong>,
          kādā
          leņķī atrodas {{ question.object3.name }}?</p>
        <!-- Komponentu un ievades lauku ietver Flexbox konteinerī -->
        <div class="d-flex justify-content-center mt-2">
          <degree-picker active-color="green" :modelValue="degrees" @update:modelValue="degrees = $event"/>
        </div>
        <div class="row align-items-center mt-2"> <!-- Pievieno rindu ar elementu vertikālo līdzināšanu -->
          <div class="col">
            <input type="number" class="form-control" v-model.number="degrees" :disabled="!question" min="0" max="360"
                   placeholder="Ievadi leņķi (0-360)"/>
          </div>
          <div class="col-auto"> <!-- Izmanto col-auto lai kolonna aizņem tikai tik vietas, cik nepieciešams saturam -->
            <button class="btn btn-primary" @click="submitAnswer" :disabled="!question || degrees === null">Iesniegt
              atbildi
            </button>
          </div>
        </div>

        <p v-if="message">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {DegreePicker} from "degree-picker";
import {ref} from "vue";
import "degree-picker/dist/style.css";

export default {
  components: {DegreePicker},
  data() {
    return {
      question: null,
      degrees: 0, // Sākotnējā stāvokļa iestatīšana
      message: '',
      startTime: Date.now(),
    };
  },
  mounted() {
    const lastAnsweredQuestionId = sessionStorage.getItem('lastAnsweredQuestionId') || null;
    this.fetchNextQuestion(lastAnsweredQuestionId);
  },
  methods: {
    fetchNextQuestion(lastAnsweredQuestionId) {
      let url = 'http://localhost:8000/perceptiontest/next_question/';
      if (lastAnsweredQuestionId) {
        url += `${lastAnsweredQuestionId}/`;
      }
      axios.get(url)
          .then(response => {
            this.question = response.data;
            this.degrees = 0; // Reset degrees
            this.message = ''; // Clear previous messages
            this.startTime = Date.now();
            console.log(response.data);
          })
          .catch(error => {
            console.error("Error fetching the question:", error);
            this.message = 'Diemžēl notika kļūda, mēģiniet vēlāk.';
          });
    },
    submitAnswer() {
      if (this.degrees < 0 || this.degrees > 360) {
        this.message = 'Lūdzu, ievadiet derīgu leņķi no 0 līdz 360 grādiem.';
        return;
      }

      const endTime = Date.now();
      const timeTaken = endTime - this.startTime;

      const answerData = {
        question: this.question.id,
        test_taker: sessionStorage.getItem('testTakerId'),
        time_taken: new Date(timeTaken).toISOString().substr(11, 8),
        user_angle: this.degrees,
        correct_angle: this.question.correct_angle,
      };

      axios.post('http://localhost:8000/perceptiontest/submit_answer/', answerData)
          .then(response => {
            this.message = "Atbilde veiksmīgi iesniegta!";
            sessionStorage.setItem('lastAnsweredQuestionId', this.question.id);
            this.fetchNextQuestion(this.question.id);
          })
          .catch(error => {
            console.error("Error submitting the answer:", error);
            this.message = "Radās problēma atbildes iesniegšanā. Lūdzu, mēģiniet vēlreiz.";
          });
    }
  }
}
</script>

<style>
/* Style adjustments */


.custom-container {
  max-width: 800px;
  margin: 0 auto;
}
</style>
