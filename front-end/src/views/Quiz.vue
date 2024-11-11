<template>
  <b-container v-if="this.features !== undefined && this.features !== null" style="min-width: 100%">
    <b-row>
      <b-text style="margin-bottom: 1rem; font-size: 20px">
        <span style="font-weight: bold; font-size: 24px">Instruction:</span> You are encouraged to participate in this quiz, which draws from the tutorials and is designed to assess your
        knowledge of the interface and task features. Successfully answering many of the questions on the assessment
        permits you to proceed with the primary phase of the user study.
      </b-text>
    </b-row>

    <div class="my-line"></div>

    <b-row>
      <b-text style="margin-bottom: 2rem; font-size: 20px">
        <span style="font-weight: bold; font-size: 24px">Question:</span> Task features are the essential aspects of task scenarios determining each plan's commute time and commute cost.
        You are given the list of features you will encounter during the user study and asked to identify which one
        explicitly affects the commute time, cost, or both.
        To accomplish this task, you can drag and drop each feature to assign it to its respective category.
      </b-text>
    </b-row>

    <b-row>
      <b-col cols="3">
        <b-card
            class="my-card"
            no-body
            border-variant="info"
            header-text-variant="white"
            header-bg-variant="info"
            header-border-variant="info"
            align="center">
          <template #header>
            <h3 class="centered-text">Features</h3>
          </template>
          <draggable :class="`list-group my-draggable-${(features.features_impact.length/4)*15}`" :list="allImpactOptions" group="impact" :move="move">
            <b-button
                v-for="element in allImpactOptions"
                class="my-button"
                pill variant="outline-info">{{element.name.replaceAll('_',' ')}}
            </b-button>
          </draggable>
        </b-card>
      </b-col>

      <b-col v-for="column in impactColumns" cols="3">
        <b-card
            class="my-card"
            no-body
            border-variant="info"
            header-text-variant="white"
            header-bg-variant="info"
            header-border-variant="info"
            align="center">
          <template #header>
            <h3 class="centered-text">{{column.name}}</h3>
          </template>

          <draggable :class="`list-group my-draggable-${(features.features_impact.length/4)*15}`" :list="column.answers" group="impact" :move="move">
            <b-button
                v-for="element in column.answers"
                :class="`my-button ${element.color}`"
                pill :variant="(element.color === '')? 'outline-info': ''">{{element.name.replaceAll('_',' ')}}
            </b-button>
          </draggable>
        </b-card>
      </b-col>
    </b-row>

    <b-row style="margin-top: 2rem;" v-if="errors.length !== 0">
      <b-row v-for="error in errors">
        <b-text v-if="error.question_type === 'features_impact'" style="margin-top: 0.2rem; background-color: #E49393; margin-left: 1rem">
          <span style="font-weight: bold; font-size: 24px"> {{error.feature.replaceAll('_' , ' ')}}: </span>
          <span style="font-size: 16px">{{error.explanation}} </span>
          <span>So the correct answer is</span> <span style="font-weight: bold; font-size: 18px"> {{error.correct_answer[0]}} </span>
          <span v-if="error.correct_answer.length===2" style="font-weight: bold; font-size: 18px" >and {{error.correct_answer[1]}}</span>
        </b-text>
      </b-row>
    </b-row>



    <b-row >
      <b-col cols="2">
        <b-button  style="margin-top: 1rem; font-size: 24px; padding: 6px 16px 6px;" @click="submit" pill variant="outline-success" size="lg">{{(this.enabled)?'Submit':'Next'}}</b-button>
      </b-col>
      <b-col v-if="this.demoSession">
        <b-button  style="margin-top: 1rem; font-size: 24px; padding: 6px 16px 6px;" @click="nextPage" pill variant="outline-success" size="lg">Next</b-button>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import draggable from 'vuedraggable';

export default {
  name: "Quiz",
  props: {
    demoSession: {
      type: Boolean,
      required: true
    },
    userId: {
      type: String,
      required: true
    },
    studyCondition: {
      type: Number,
      required: true
    },
  },
  display: "Two Lists",
  order: 1,
  components: {
    draggable
  },
  data() {
    return {
      enabled: true,
      features: null,
      allImpactOptions: [],
      errors: [],
      impactColumns:[
        { name:'Cost', answers:[] },
        { name:'Time', answers:[] },
        { name:'Cost and Time', answers:[] },
      ],
      quiz_response: {
        features_impact:  [],
      },
    };
  },
  methods: {
    nextPage: function(){
      this.$emit('submit', {});
    },
    move: function (evt, originalEvent){
      return this.enabled;
    },
    updateBackend: async function (url, quiz_response){
      const body = {
        "user_id": this.userId,
        "study_condition": this.studyCondition,
      };

      if (quiz_response !== undefined){
        body.quiz_response = quiz_response;
      }

      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
      };
      const res = await fetch(`${window.location.origin}/api/${url}`, requestOptions);
      return  await res.json();
    },
    generateAllOptions: function (origin, color){
      const arr = [];

      for (let i = 0; i < origin.length; i++) {
        arr.push({
          name: origin[i],
          id: i,
          color: color,
        })
      }

      return arr;
    },
    getTypeUserAnswer: function (name){
      return (name === 'Time Dependent') ? 'time_dependent' : 'time_independent'
    },
    getImpactUserAnswer: function (name){
      if(name === 'Cost' ){
        return ['cost']
      } else if (name === 'Time') {
        return ['time'];
      }

      return ['cost','time'];
    },
    generateUserAnswerList: function (arr, getUserAnswer){
      const answers = [];
      let element;

      for (let i = 0; i < arr.length; i++) {
        element = arr[i];
        for (let j = 0; j < element.answers.length; j++) {
          answers.push({
            "feature": element.answers[j].name,
            "user_answer" : getUserAnswer(element.name),
          })
        }
      }

      return answers;
    },
    getColorFor: function (name , questionType, err){
      for (let i = 0; i < err.length; i++) {
        if(err[i].feature === name && err[i].question_type === questionType )
          return 'btn-red';
      }
      return 'btn-green';
    },
    updateColors: function (arr, questionType, err){
      let element;

      for (let i = 0; i < arr.length; i++) {
        element = arr[i];
        for (let j = 0; j < element.answers.length; j++) {
          element.answers[j].color = this.getColorFor(element.answers[j].name, questionType, err);
        }
      }
    },
    failed: async function(){
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Failed',
        text: 'Unfortunately, you\'ve failed the quiz, it is not possible to continue the study! Click on the Accept button to return to the Prolific.',
        accept:this.backToProlificRejected,
        close:this.failed,
        cancel:this.failed,
      })
    },
    backToProlificRejected: function (){
      window.location.href = String(import.meta.env.VITE_PROLIFIC_REJECT_LINK).toLowerCase();
    },
    submit: async function () {
      if (!this.enabled){
        this.nextPage();
        return;
      }


      this.quiz_response.features_impact = this.generateUserAnswerList(this.impactColumns, this.getImpactUserAnswer);

      const res = await this.updateBackend('check_user_qualification', this.quiz_response);

      if (res.status === 'failed'){
        localStorage.setItem('failed', 'true');
        await this.failed();
        return
      }

      if (res.errors.length === 0){
        this.nextPage();
        return
      }

      this.errors = res.errors;
      this.enabled = false;

      this.updateColors(this.impactColumns, 'features_impact', res.errors);
    },
  },
  created: async function(){
    this.features = await this.updateBackend('get_user_quiz')
    this.allImpactOptions = this.generateAllOptions(this.features.features_impact, "");
  }
};
</script>

<style scoped>

.centered-text {
  text-align: center;
  font-size: 2.5rem;
}

.my-button {
  padding: 0.5rem 0.2rem 0.5rem;
  margin: 0.5rem 10% 0.5rem;
  font-size: 1rem;
  width: 70%;
}

.my-draggable-15 {
  height: 15rem;
}

.my-draggable-30 {
  height: 30rem;
}

.my-draggable-45 {
  height: 45rem;
}

.my-card {
  min-height: 100%;
  border-radius: 1.25rem;
}

.my-card >>> div {
  border: 1rem;
  border-radius: 1rem 1rem 0 0;
  padding-bottom: 0;
  padding-left: 0;
  padding-right: 0;
}

.my-line {
  border: 2px solid #d2d2d2;
  margin: 1rem 0 1rem;
  border-radius: 5px;
  min-width: 100%;
}

.btn-red, .btn-red:hover, .btn-red:active, .btn-red:visited {
  border: 2px solid #a21e1e;
  background-color: #a21e1e !important;
}

.btn-green, .btn-green:hover, .btn-green:active, .btn-green:visited {
  border: 2px solid #1ea243;
  background-color: #1ea243 !important;
}
</style>