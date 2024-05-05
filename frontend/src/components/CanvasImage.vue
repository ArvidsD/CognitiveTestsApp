<template>
  <div class="container ">
    <div class="d-flex justify-content-center ">
      <canvas class="imageCanvas" ref="imageCanvas" width="600" height="500" style="">
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
      images: [],
    };
  },
  mounted() {
    this.loadImages();
  },
  methods: {
    loadImages() {
      const apiUrl = import.meta.env.VITE_DJANGO_SERVER_URL + '/perceptiontest/imageobjects/';
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
            context.drawImage(imageObj, img.x_coordinate, img.y_coordinate, 100, 100);
          };

          imageObj.src = import.meta.env.VITE_DJANGO_SERVER_URL + `/${img.image_url}`;
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
  aspect-ratio: 600 / 500;
  display: block;
  margin: 0 auto;
}
</style>
