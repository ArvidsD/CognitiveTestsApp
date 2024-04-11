<template>
  <div class="container">
    <div class="container mt-5">
      <h1 class="text-center">Perspektīves tests</h1>
      <p>Pirms testa sākšanas, aizpildi personīgo informāciju</p>

    </div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="text" class="form-control" id="firstName" v-model="form.firstName" required>
      </div>
      <div class="form-group">
        <label for="age">Age</label>
        <input type="number" class="form-control" id="age" v-model="form.age" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" class="form-control" id="email" v-model="form.email" required>
      </div>
      <button type="submit" class="btn btn-primary">Start Test</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        firstName: '',
        age: null,
        email: '',
        takenTest: 'Perception test'
      }
    };
  },
  methods: {
    submitForm() {
      // Notīrīt sesiju pirms jauna testa sākuma
      sessionStorage.clear();
      const apiUrl = 'http://localhost:8000/perceptiontest/testtaker/';

      axios.post(apiUrl, {
        first_name: this.form.firstName,
        age: this.form.age,
        email: this.form.email,
        takenTest: this.form.takenTest
      })
          .then(response => {
            // Saglabājiet test_taker_id lokāli, lai to varētu izmantot atbildēs
            sessionStorage.setItem('testTakerId', response.data.id);
            // Pāradresējiet lietotāju uz jautājumu lapu vai parādiet apstiprinājumu
            console.log(response.data);
            // Pāradresēšanas piemērs, ja nepieciešams:
            // this.$router.push({ name: 'questionPage' });
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
/* Jūsu CSS stilu definīcijas, ja nepieciešams */
</style>
