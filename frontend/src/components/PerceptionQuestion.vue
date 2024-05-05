<template>
  <div>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <p v-if="question" class="text-center">Iedomājies, ka esi <strong>{{ question.object1.name }}</strong> un
          skaties uz
          <strong>{{ question.object2.name }}</strong>,
          kādā
          leņķī atrodas <strong>{{ question.object3.name }}?</strong></p>
        <div class="d-flex flex-column align-items-center"><p v-if="question" style="height: 0px;">
          {{ question.object2.name }}</p>
          <p style="height: 0px;
        position: relative;
        top: 132px;
        z-index: 100;" v-if="question">{{ question.object1.name }}</p>
        </div>

        <div class="d-flex justify-content-center">


          <degree-picker active-color="black" :modelValue="degrees" width="220px" step="360"
                         @update:modelValue="degrees = $event"/>
          <div class="vl"></div>
        </div>
        <div class="row align-items-center mt-2 justify-content-center">
          <div class="col-auto">
            <input type="number" class="form-control hidden" v-model.number="degrees"
                   :disabled="!question" min="0" max="360"
                   placeholder="Ievadi leņķi (0-360)"/>
            <button class="btn btn-secondary" @click="submitAnswer" :disabled="!question || degrees === null">Iesniegt
              atbildi
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {DegreePicker} from "degree-picker";

import "degree-picker/dist/style.css";

export default {
  components: {DegreePicker},
  data() {
    return {
      question: null,
      degrees: 0,
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
      let url = import.meta.env.VITE_DJANGO_SERVER_URL + '/perceptiontest/next_question/';
      if (lastAnsweredQuestionId) {
        url += `${lastAnsweredQuestionId}/`;
      }
      axios.get(url)
          .then(response => {
            if (response.data.message === "finished") {

              this.message = "Paldies, ka piedalījāties testā!";
              this.question = null; // Tīrīt jautājumu
              sessionStorage.setItem('isTestCompleted', 'true');
              this.$emit('test-completed');
            } else {
              this.question = response.data;
              this.degrees = 0;
              this.message = '';
              this.startTime = Date.now();
            }
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

      axios.post(import.meta.env.VITE_DJANGO_SERVER_URL + 'perceptiontest/submit_answer/', answerData)
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
.vl {
  border-left: 2px solid black;
  height: 103px;
  position: absolute;
  z-index: 2;
  margin-top: 10px;
}
.hidden{
  display: none;
}
</style>
