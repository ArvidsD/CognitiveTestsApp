<template>
  <div class="container mt-4">
    <h2>Demogrāfisko datu aptauja</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="gender">Dzimums:</label>
        <select v-model="formData.gender" class="form-control">
          <option value="">Lūdzu izvēlieties...</option>
          <option value="Male">Vīrietis</option>
          <option value="Female">Sieviete</option>

        </select>
      </div>

      <div class="form-group">
        <label for="age">Vecums:</label>
        <input type="number" v-model.number="formData.age" class="form-control" placeholder="Ievadiet vecumu"/>
      </div>

      <div class="form-group">
        <label for="nativeLanguage">Dzimtā valoda:</label>
        <select v-model="formData.native_language" class="form-control">
          <option value="">Lūdzu izvēlieties...</option>
          <option value="Latvian">Latviešu</option>
          <option value="Russian">Krievu</option>
          <option value="Other">Cita</option>
        </select>
        <!-- Ļauj ievadīt citu valodu, ja izvēlēta opcija "Cita" -->
        <input v-if="formData.native_language === 'Other'" v-model="formData.other_language"
               placeholder="Norādiet valodu" class="form-control"/>
      </div>

      <div class="form-group">
        <label>Izglītības līmeņi:</label>
        <div v-for="level in educationOptions" :key="level.id">
          <label>
            <input type="checkbox" :value="level.name" v-model="formData.education_levels">
            {{ level.name }}
          </label>
        </div>
      </div>

      <div class="form-group">
        <label>Nodarbošanās:</label>
        <div v-for="profession in professionOptions" :key="profession.id">
          <label>
            <input type="checkbox" :value="profession.name" v-model="formData.professions">
            {{ profession.name }}
          </label>
        </div>
        <label>
          <input type="checkbox" value="Other" v-model="otherProfessionChecked">
          Cits
        </label>
        <input v-if="otherProfessionChecked" v-model="formData.other_profession" placeholder="Norādiet nodarbošanos"
               class="form-control"/>
      </div>

      <div class="form-group">
        <label for="dominantHand">Dominējošā roka:</label>
        <select v-model="formData.dominant_hand" class="form-control">
          <option value="">Lūdzu izvēlieties...</option>
          <option value="Left">Kreilis</option>
          <option value="Right">Labrocis</option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Iesniegt</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        test_taker: sessionStorage.getItem('testTakerId'),
        gender: '',
        age: null,
        native_language: '',
        education_levels: [],
        professions: [],
        other_profession: '',  // Saglabāt vērtību, ja izvēlēts "Cits"
        dominant_hand: '',
      },
      educationOptions: [
        {id: 1, name: "Pamatskola"},
        {id: 2, name: "Vidusskola"},
        {id: 3, name: "Vidējā - profesionālā izglītība"},
        {id: 4, name: "Augstākā izglītība – bakalaurs"},
        {id: 5, name: "Augstākā izglītība – maģistrs"},
        {id: 6, name: "Augstākā izglītība – doktors"}],
      professionOptions: [
        {id: 1, name: "Augstākā vai vidējā līmeņa vadītājs"},
        {id: 2, name: "Speciālists, ierēdnis, nestrādā fizisku darbu"},
        {id: 3, name: "Strādnieks, strādā fizisku darbu"},
        {id: 4, name: "Zemnieks (ir sava zemnieku saimniecība)"},
        {id: 5, name: "Ir savs uzņēmums, individuālais darbs"},
        {id: 6, name: "Pensionārs (-e)"},
        {id: 7, name: "Skolnieks, students"},
        {id: 8, name: "Mājsaimniece (-ks), bērna kopšanas atvaļinājums"},
        {id: 9, name: "Bezdarbnieks"}
      ],
      otherProfessionChecked: false  // Pārvaldīt, vai "Cits" ir atzīmēts
    };
  },
  mounted() {
    if (!sessionStorage.getItem('demographicsInitialized')) {
      this.initializeDemographics();
    }
  },
  methods: {
    initializeDemographics() {
      const url = `http://localhost:8000/perceptiontest/submitdemographic/`;
      const initialData = {test_taker: this.formData.test_taker};
      axios.post(url, initialData)
          .then(response => {
            console.log('Demographic record initialized:', response.data);
            // Iestatiet karodziņu sesijas krātuvē, lai norādītu, ka inicializācija ir notikusi
            sessionStorage.setItem('demographicsInitialized', 'true');
          })
          .catch(error => {
            console.error('Error initializing demographic data:', error);
          });
    },
    handleSubmit() {
      // First, make a copy of the current professions without modifying the original array
      let professions = [...this.formData.professions];

      // Check if "Other" profession was entered and transform it to uppercase if it was
      if (this.otherProfessionChecked && this.formData.other_profession) {
        const otherProfession = this.formData.other_profession.toUpperCase();
        // Add the "other profession" to the professions array if not already included
        if (!professions.some(profession => profession.name === otherProfession)) {
          professions.push({name: otherProfession});
        }
      }

      // Transform all existing profession strings in the array to uppercase objects with a 'name' key
      professions = professions.map(profession => {
        if (typeof profession === 'string') {
          return {name: profession.toUpperCase()};
        }
        return {name: profession.name.toUpperCase()};
      });

      // Similarly, transform all the education_levels to uppercase objects with a 'name' key
      const education_levels = this.formData.education_levels.map(level => {
        return {name: level.toUpperCase()};
      });

      // Now, build the final data object to send
      const dataToSend = {
        ...this.formData,
        education_levels: education_levels,
        professions: professions,
        // Remove the 'other_profession' field as it's now included in the professions array
      };
      delete dataToSend.other_profession;

      // Make the PUT request with the transformed data object
      const url = `http://localhost:8000/perceptiontest/submitdemographic/${this.formData.test_taker}/`;
      axios.put(url, dataToSend)
          .then(response => {
            alert('Data successfully submitted');
            sessionStorage.clear();
            this.$router.push('/');
          })
          .catch(error => {
            console.error('Error submitting the data:', error);
            alert('Error submitting the data');
          });
    }
  }
};
</script>

<style>
.form-group {
  margin-bottom: 15px;
}
</style>
