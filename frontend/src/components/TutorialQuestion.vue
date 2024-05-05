<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="d-flex justify-content-center">
          <canvas class="imageCanvas" ref="imageCanvas" width="800" height="600">
            Your browser does not support the canvas element.
          </canvas>
        </div>
        <p v-if="question">Iedomājies, ka esi <strong>{{ question.object1.name }}</strong> un skaties uz
          <strong>{{ question.object2.name }}</strong>,
          kādā leņķī atrodas <strong>{{ question.object3.name }}?</strong></p>
        <div class="d-flex flex-column align-items-center "><p v-if="question" style="height: 0px;">

          {{ question.object2.name }}</p>

          <p style="height: 0px;
        position: relative;
        top: 132px;
        z-index: 100;" v-if="question">{{ question.object1.name }}</p>
        </div>
        <div class="d-flex justify-content-center">

          <degree-picker active-color="black" :modelValue="degrees" width="220px"
                         @update:modelValue="degrees = $event" step="360">  </degree-picker>
          <div class="vl"></div>
        </div>
        <div class="row align-items-center mt-2">
          <div class="col">
            <input type="number" class="form-control" v-model.number="degrees" :disabled="!question" min="0" max="360"
                   placeholder="Ievadi leņķi (0-360)"/>
          </div>
          <div class="col-auto">
            <button class="btn btn-secondary" @click="submitAnswer" :disabled="!question || degrees === null">Izmēģināt
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
import {DegreePicker} from "degree-picker";
import "degree-picker/dist/style.css";

export default {
  components: {DegreePicker},
  data() {
    return {
      question: {
        id: 1,
        object1: {name: "Koks", x: 50, y: 50},
        object2: {name: "Māja", x: 100, y: 150},
        object3: {name: "Auto", x: 60, y: 200},
        correct_angle: 120
      },
      degrees: 0,
      message: '',
      images: [
        {src: 'koks.png', x: 50, y: 50},
        {src: 'maja.png', x: 100, y: 150},
        {src: 'mašīna.png', x: 60, y: 200},
        {src: 'puķe.png', x: 200, y: 75}
      ]
    };
  },
  mounted() {
    this.drawImages();
  },
  methods: {
    drawImages() {
      const canvas = this.$refs.imageCanvas;
      if (canvas) {
        const context = canvas.getContext('2d');
        this.images.forEach(img => {
          const imageObj = new Image();
          imageObj.onload = () => {
            context.drawImage(imageObj, img.x, img.y, 100, 100);
          };
          imageObj.src = `/${img.src}`;
        });
      }
    },
    submitAnswer() {
      if (this.degrees < 0 || this.degrees > 360) {
        this.message = 'Lūdzu, ievadiet derīgu leņķi no 0 līdz 360 grādiem.';
        return;
      }
      this.message = `Tu ievadīji ${this.degrees} grādus. Pareizā atbilde ir ${this.question.correct_angle} grādi.`;
    }
  }
}
</script>

<style scoped>
.imageCanvas {
  max-width: 100%;
  height: auto;
  aspect-ratio: 800 / 600;
  display: block;
  margin: 0 auto;
}

.vl {
    border-left: 2px solid black;
    height: 103px;
    position: absolute;
    z-index: 2;
    margin-top: 10px;
}

</style>
