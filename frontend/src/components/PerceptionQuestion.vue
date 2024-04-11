<template>
  <div class="question-container">
    <h2>Jautājums</h2>
    <p v-if="question">Iedomājies, ka esi {{ question.object1.name }} un skaties uz {{ question.object2.name }}, kādā
      leņķī atrodas {{ question.object3.name }}?</p>
    <input type="number" v-model.number="answer" :disabled="!question" min="0" max="360"
           placeholder="Ievadi leņķi (0-360)"/>
    <button @click="submitAnswer" :disabled="!question || answer === null">Iesniegt atbildi</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      question: null,
      answer: null,
      message: '',
      startTime: Date.now(), // Sākuma laiks atbildes taimera uzsākšanai
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
            this.answer = null; // Reset answer field
            this.message = ''; // Clear previous messages
            this.startTime = Date.now(); // Atjaunojiet sākuma laiku
          })
          .catch(error => {
            console.error("Error fetching the question:", error);
            this.message = 'Diemžēl notika kļūda, mēģiniet vēlāk.';
          });
    },
    submitAnswer() {
      if (this.answer < 0 || this.answer > 360) {
        this.message = 'Lūdzu, ievadiet derīgu leņķi no 0 līdz 360 grādiem.';
        return;
      }

      const endTime = Date.now();
      const timeTaken = endTime - this.startTime; // Aprēķina laiku milisekundēs

      const answerData = {
        question: this.question.id,
        test_taker: sessionStorage.getItem('testTakerId'), // Izmantojiet saglabāto test_taker ID no sessionStorage
        time_taken: new Date(timeTaken).toISOString().substr(11, 8), // Konvertē uz HH:MM:SS formātu
        user_angle: this.answer,
        correct_angle: this.question.correct_angle,
      };

      axios.post('http://localhost:8000/perceptiontest/submit_answer/', answerData)
          .then(response => {

            this.message = "Atbilde veiksmīgi iesniegta!";
            sessionStorage.setItem('lastAnsweredQuestionId', this.question.id); // Saglabājiet pēdējo atbildēto jautājumu ID
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
/* Add your styles here */
.question-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
