<script setup>
import PreTest from './PreTest.vue'
import Test from './Test.vue'
import Quiz from './Quiz.vue'
import PostTest from './PostTest.vue'
</script>

<template>
  <b-card class="my-card" no-body>
    <b-tabs v-if="currentPage" card>
      <b-tab :title="this.currentPage.title" >
        <PreTest v-if="pages.pretest.show" :demoSession="demoSession" @submit="done"></PreTest>
        <Test v-else-if="pages.demo.show" :demoSession="demoSession" :demoTab="true" @nextTab="done"></Test>
        <Test v-else-if="pages.onboarding.show" :demoSession="demoSession" :onBoarding="true" @onBoardingFinished="done"></Test>
        <Test v-else-if="pages.tutorial.show" :demoSession="demoSession" :tutorial="true" @tutorialFinished="done"></Test>
        <Test v-else-if="pages.training.show" :demoSession="demoSession" :training="true" @trainingFinished="done"></Test>
        <Quiz v-else-if="pages.quiz.show" :demoSession="demoSession" :userId="userId" :studyCondition="studyCondition" @submit="done"></Quiz>
        <Test v-else-if="pages.maintask.show" :demoSession="demoSession" :mainTasks="true" @mainTasksFinished="done"></Test>
        <PostTest v-else-if="pages.posttest.show" :demoSession="demoSession" @submit="done"></PostTest>
        <div v-else-if="pages.score.show">
          <b-row>
            <b-text style="font-size: 24px">
              Thank you for taking part in our research! Your total points obtained are <span style="font-weight: bold">{{this.getScore()}}</span>.
            </b-text>
            <br/>
            <b-text v-if="getScore() !== '0'" style="font-size: 24px">
              Rest assured that your hard work will not go unrewarded, and we will add a benefit to your prolific account based on your score within two weeks.
            </b-text>
            <b-text v-else style="font-size: 24px">
              As a participant in the study, you will receive remuneration according to the time invested. This compensation will be provided within two weeks.
            </b-text>
          </b-row>
          <b-row>
            <b-button  style="margin-top: 1rem; font-size: 24px; padding: 6px 16px 6px;" @click="backToProlificAccepted" pill variant="outline-success" size="lg">Return to Prolific</b-button>
          </b-row>
        </div>
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
export default {
  name: "MainWindow",
  data() {
    return {
      userId: undefined,
      currentPage: undefined,
      studyCondition: undefined,
      complexity: undefined,
      taskType: undefined,
      demoSession: String(import.meta.env.VITE_DEMO_SESSION).toLowerCase() === "true",
      pages: { // todo move it to file
        pretest:{
          show: false,
          title: 'Pre Test',
          next: 'unknown',
        },
        demo:{
          show: false,
          title: 'Demo',
          next: 'onBoarding',
        },
        onboarding:{
          show: false,
          title: 'OnBoarding',
          next: 'tutorial',
        },
        tutorial:{
          show: false,
          title: 'Tutorial',
          next: 'training',
        },
        training:{
          show: false,
          title: 'Training',
          next: 'quiz',
        },
        quiz:{
          show: false,
          title: 'Quiz',
          next: 'mainTask',
        },
        maintask:{
          show: false,
          title: 'Main Tasks',
          next: 'postTest',
        },
        posttest:{
          show: false,
          title: 'Post Test',
          next: 'score',
        },
        score:{
          show: false,
          title: 'Score',
        },
      },
    }
  },
  methods :{
    updateBackend: async function (url, body) {
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
      };
      const res = await fetch(`${window.location.origin}/api/${url}`, requestOptions);
      return await res.json();
    },
    getScore: function (){
      return localStorage.getItem(`${this.userId}-score`);
    },
    done: async function ( body ){
      // TODO loading
      let next = this.currentPage.next;

      if (this.currentPage.next === 'unknown'){
        const res = await this.updateBackend('get_user_tutorial', body);
        if (res.status !== 'passed'){
          localStorage.setItem('failed', 'true');
          await this.failed();
          return
        }
        const info = {
          study_condition: res.study_condition,
          complexity: res.complexity,
          task_type: res.task_type,
        }
        localStorage.setItem(`${this.userId}-info`, JSON.stringify(info));
        next = (this.demoSession)? 'demo' : 'onBoarding';
      }

      localStorage.setItem(`${this.userId}-progress`, next);

      await this.$router.push(`/${this.userId}/${next}`);
    },
    failed: async function(){
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Failed',
        text: 'Unfortunately, you\'ve failed the attention checks, it is not possible to continue the study! Click on the Accept button to return to the Prolific.',
        accept:this.backToProlificRejected,
        close:this.failed,
        cancel:this.failed,
      })
    },
    backToProlificAccepted: function (){
      window.location.href = String(import.meta.env.VITE_PROLIFIC_ACCEPT_LINK).toLowerCase();
    },
    backToProlificRejected: function (){
      window.location.href = String(import.meta.env.VITE_PROLIFIC_REJECT_LINK).toLowerCase();
    }
  },
  mounted: async function (){
    const failed = localStorage.getItem('failed');
    if (failed === 'true'){
      await this.failed();
    }

    const page = this.$route.path.split('/')[2].toLowerCase(); // todo, this line may cause bug in the future.
    const userId = this.$route.params.userId;

    const progress = localStorage.getItem(`${userId}-progress`);

    // todo You may remove the following lines
    const userInfo = JSON.parse(localStorage.getItem(`${userId}-info`));
    if(userInfo !== null){
      this.studyCondition= parseInt(userInfo.study_condition);
      this.complexity= userInfo.complexity;
      this.taskType= userInfo.task_type;
    }

    if (progress.toLowerCase() !== page.toLowerCase()){
      await this.$router.push(`/${userId}/${progress}`);
      return;
    }

    this.userId = userId;
    this.currentPage = this.pages[page];

    if (this.currentPage === undefined || this.userId === undefined){
      await this.$router.push('/');
      this.$vs.notify({
        title:'Invalid URL',
        text:'You don\'t have access to this url',
        color:`rgb(72, 162, 211)`
      });
    }

    this.currentPage.show = true;
  }
}
</script>

<style scoped>
.my-card {
  margin: 2%;
}

</style>