<template>
  <div>
    <h1 class="text-center">Uzdevums</h1>
    <p>
      <ul>
        <li>Tests sastāv no 12 uzdevumiem.</li>
        <li>Katrā no uzdevumiem Jūs redzēsiet attēlu ar objektiem un apli, kurā jāatzīmē leņķis starp 3 dažiem dotā
          attēla objektiem.
        </li>
        <li>Vajadzēs iztēloties, ka stāvat pie viena no dotā attēla objektiem (nosaukts apļa centrā) un esat vērsts pret
          citu objektu (nosaukts apļa augšpusē).
        </li>
        <li>Jūsu uzdevums būs atzīmēt leņķi uz riņķa līnijas, parādot virzienu uz trešo objektu attiecībā no sevis.</li>
      </ul>
    </p>

    <TutorialQuestion class="mb-5"/>


    <form @submit.prevent="submitForm">
      <div class="text-center">
        <button type="submit" class="btn btn-secondary mb-5">Sākt Testu</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import TutorialQuestion from "@/components/TutorialQuestion.vue";

export default {
  components: {TutorialQuestion},
  data() {
    return {
      form: {
        takenTest: 'Perception test',
        session_id: ''
      }
    };
  },

  methods: {
    submitForm() {
      sessionStorage.clear();
      this.form.session_id = `sess-${Date.now()}`;

      const apiUrl = import.meta.env.VITE_DJANGO_SERVER_URL + '/perceptiontest/testtaker/';
      axios.post(apiUrl, this.form)
          .then(response => {
            sessionStorage.setItem('testTakerId', response.data.id);
            console.log(response.data);
          })
          .catch(error => {
            console.error("There was an error submitting the form:", error);
          });
      this.$emit('form-submitted');
    }
  }
}
</script>

<style>

</style>
