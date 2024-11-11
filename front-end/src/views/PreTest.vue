<script setup>
import Radio from '../components/Radio.vue'
import Range from '../components/Range.vue'
</script>

<template>
  <div>
    <b-row style="margin-bottom: 1rem">
      <b-col>
        <b-button v-if="currentPage !== 4" class="mt-2" align-h="right" @click="nextQuestions()" pill variant="outline-success" size="lg">Next</b-button>
        <b-button v-if="currentPage === 4" class="mt-2" align-h="right" @click="submit()" pill variant="outline-success" size="lg">Submit</b-button>
      </b-col>
      <b-col align="right" v-if="demoSession">
        <b-button class="mt-2" align-h="right" @click="nextTab()" pill variant="outline-success" size="lg">Next Tab</b-button>
      </b-col>
    </b-row>

    <div id="my-questions" v-for="(question, index) in questions.slice(currentQuestionsIndexes.first, currentQuestionsIndexes.last)" :key="question.question" >
      <Radio
          v-if="question.answer_list.length !== 2"
          :index="(currentPage-1)* 5 + index"
          :question="question.question"
          :options="question.answer_list"
          :becomeRedIfEmpty="becomeRedIfEmpty"
          @selectedChanged="selectedChanged">
      </Radio>
      <Range
          v-else-if="question.answer_list.length === 2"
          :index="(currentPage-1)* 5 + index"
          :question="question.question"
          :max="question.likert_scale"
          :beginningLabel="question.answer_list[0]"
          :endLabel="question.answer_list[1]"
          :becomeRedIfEmpty="becomeRedIfEmpty"
          @selectedChanged="selectedChanged">
      </Range>
    </div>

    <b-row style="margin-bottom: 1rem">
      <b-col>
        <b-button v-if="currentPage !== 4" class="mt-2" align-h="right" @click="nextQuestions()" pill variant="outline-success" size="lg">Next</b-button>
        <b-button v-if="currentPage === 4" class="mt-2" align-h="right" @click="submit()" pill variant="outline-success" size="lg">Submit</b-button>
      </b-col>
      <b-col align="right" v-if="demoSession">
        <b-button class="mt-2" align-h="right" @click="nextTab()" pill variant="outline-success" size="lg">Next Tab</b-button>
      </b-col>
    </b-row>

  </div>
</template>

<script>
import questions from '../questions/pre_test.json';

export default {
  name: "PreTest",
  props: {
    demoSession: {
      type: Boolean,
      required: true
    },
  },
  data() {
    return {
      currentPage: 1,
      becomeRedIfEmpty: false,
      user_id: null,
      questions: questions,
      answers: new Array(questions.length).fill(-1),
    }
  },
  methods:{
    nextTab: function (){
      if(this.demoSession){
        const data = this.generateFinalAnswers();
        this.$emit('submit', data);
      }
    },
    nextQuestions: function (){
      const firstIndex = this.currentQuestionsIndexes.first;
      const lastIndex = this.currentQuestionsIndexes.last;
      if(!this.answeredAllQuestions(firstIndex,lastIndex)){
        this.becomeRedIfEmpty = true;
        this.$vs.notify({
          title:'Not completed',
          text:'Please answer all questions.',
          color:`rgb(211,72,93)`
        });
        return;
      }

      this.becomeRedIfEmpty = false;
      this.currentPage += 1;
    },
    selectedChanged: function (obj){
      this.answers[obj.index] = (obj.type === 'Range') ? parseInt(obj.answer) : obj.answer + 1;
      // console.log(this.answers);
    },
    generateFinalAnswers: function (){
      const result = []

      for (let i=0; i< this.questions.length; i++){
        result.push({
          question_id: this.questions[i].question_id,
          answer: this.answers[i]
        });
      }

      return {
        "user_id": this.user_id,
        "pre_test": JSON.stringify(result)
      };
    },
    submit: async function () {
      if(this.answeredAllQuestions(0,this.questions.length)){
        const data = this.generateFinalAnswers();
        this.$emit('submit', data);
        return
      }

      this.becomeRedIfEmpty = true;
      this.$vs.notify({
        title:'Not completed',
        text:'Please answer all questions.',
        color:`rgb(211,72,93)`
      });
    },
    answeredAllQuestions: function (firstIndex, lastIndex){
      for (let i = firstIndex; i < lastIndex; i++) {
        if(this.answers[i] === -1){
          return false;
        }
      }
      return true;
    }
  },
  computed: {
    currentQuestionsIndexes: function (){
      const first = (this.currentPage -1) * 5;
      const last = (this.currentPage === 4) ? this.questions.length : (this.currentPage) * 5;
      return {
        first: first,
        last: last
      };
    }
  },
  created: function () {
    this.user_id = this.$route.params.userId
  }
}
</script>

<style scoped>

</style>