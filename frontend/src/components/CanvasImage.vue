<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-center">
      <canvas class ="imageCanvas" ref="imageCanvas" width="800" height="600" style="border:1px solid #000000;">
        Your browser does not support the canvas element.
      </canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ImageCanvas',
  data() {
    return {
      images: [], // Saglabājiet attēlus kā objektus
    };
  },
  mounted() {
    this.loadImages();
  },
  methods: {
    loadImages() {
      const apiUrl = 'http://localhost:8000/perceptiontest/imageobjects/';
      axios.get(apiUrl).then(response => {
        this.images = response.data;
        this.drawImages();
      }).catch(error => {
        console.error("There was an error fetching the images:", error);
      });
    },
    drawImages() {
      const canvas = this.$refs.imageCanvas;
      if (canvas && this.images.length) {
        const context = canvas.getContext('2d');
        this.images.forEach(img => {
          const imageObj = new Image();
          imageObj.onload = () => {
            context.drawImage(imageObj, img.x_coordinate, img.y_coordinate, 70, 70);
          };
          // Pievienojiet pilno ceļu līdz attēla avotam
          imageObj.src = `http://localhost:8000/static/${img.image_url}`;
        });
      }
    }
  }
}
</script>
<style scoped>
.imageCanvas {
  max-width: 100%;
  height: auto;
  aspect-ratio: 800 / 600; /* Saglabājiet oriģinālo proporciju, pieņemot, ka jūsu oriģinālais izmērs ir 800x600 */
  border: 1px solid #000000;
  display: block; /* Lai nodrošinātu, ka tiek ievērots augstums atkarībā no platuma */
  margin: 0 auto; /* Centrēšanai */
}
</style>
