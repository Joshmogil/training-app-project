<template>
  <div class="Setup">
    
    
    <div class="big-container">
        <div class="container">
            <h1>Setup</h1>
        </div>


        <div class="container">
            <div class = "option" v-for="(goal, index) in $store.state.allGoals" :key="`goal-${index}`">{{goal}}</div>
        </div>
        
        

        <div class="container">
            <div class = "option" v-for="(split, index) in $store.state.allSplits" :key="`split-${index}`">{{split}}</div>
        </div>
        
        

        <div class="container">
            <div class = "option" v-for="(day, index) in $store.state.days" :key="`split-${index}`">{{day}}</div>
        </div>
        
        

        <div class="container">
            <div class = "option" v-for="(choice, index) in $store.state.cardio" :key="`split-${index}`">{{choice}}</div>    
        </div>
    </div>

    
    

    
  </div>
</template>

<script>
import dynamicDbService from "../services/DynamicDBService";

export default {
  name: "setup",
  data() {
    return {
      newSettings: {
        user_id: this.$store.state.user.user_id,
        goal: "string",
        split: 0,
        preffered_days: "string",
        cardio: true
        }
    };

  },
  methods: {
    getGoalsAndSettings() {
      dynamicDbService
        .getGoalsAndSplits()
        .then(response => {
          if (response.status == 200) {
            this.$store.commit("SET_GOALS", response.data.goals);
            this.$store.commit("SET_SPLITS", response.data.splits);

          }
        })
        .catch(error => {
          error == error

        });
    }
  },
  beforeMount(){
    this.getGoalsAndSettings()
  }
};


</script>

<style>

.container {
  display: flex; /* or inline-flex */
  gap: 1vw;
  justify-content: center;
  justify-content: space-evenly;
}

.big-container {
  display: flex; /* or inline-flex */
  flex-direction: column;
  gap: 2vw;
  height: 80vh;
  justify-content: center;
  justify-content: space-evenly;
}

div.container{
    flex-grow: 1;
}

.option{
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size:110%;
}

</style>