<template>
  <b-container class="container">
    <b-card :img-src="require('@/assets/map_intro.jpeg')"
            img-alt="Image"
            img-height="300rem"
            img-top
            class="card"
            title="Plan your entire trip with us!">

      <b-card-text>
        Thank you for taking the time to explore our experiment.
        Before you read more about this experiment, we'd like to draw your attention to three important points.
      </b-card-text>

      <b-card-text>
        We ask you to answer our pre and post questionnaires truthfully (to the best of your knowledge) - we will not penalize you for getting a question incorrect!
        We are merely interested in examining your experience of using our interface and doing the task.
      </b-card-text>

      <b-card-text>
        As a reward for presenting the best response concerning our primary investigation comprising three different task scenarios, we intend to grant you supplementary compensation.
        Further elaboration regarding this matter will be deliberated subsequently.
      </b-card-text>

      <b-card-text>
        Please refrain from pushing the back button in your browser throughout this study.
        Use the Next buttons found in our system’s interface instead.
      </b-card-text>




      <b-card-text>
        This task should take approximately <b>40-50 minutes </b> of your time and consists of seven stages. We outline the seven stages below.
      </b-card-text>

      <b-card-text>
        In the <b> first </b> stage of the experiment, you will be asked some questions about your basic numeracy skill and interaction with technical systems (apps, software applications, and digital devices such as mobile phones, car navigation, computer, TV.)
      </b-card-text>

      <b-card-text>
        Following this, in the <b> second </b>stage, you will be presented with our interface tutorial to learn about the functionality of different components.
      </b-card-text>

      <b-card-text>
        In the <b> third </b> stage, you will be presented with the task tutorial which you’ll figure out the details of scenarios and variables you need to take into account.
      </b-card-text>

      <b-card-text>
        Upon completion of tutorials, in the <b> fourth </b> stage, you will be presented with our interface to train with the example shown in tutorial sections.
        You can learn how to work with the system by practicing on the example.
        You can move to the next stage when you submit your final decision.
      </b-card-text>

      <b-card-text>
        In the <b> fifth </b> stage, you are given a quiz based on the tutorials to ensure you have sufficiently explored the interface and task features.
        You become entitled to continue the main study upon answering most quiz questions correctly.
      </b-card-text>

      <b-card-text>
        In the <b> sixth </b> stage, you will be directed to the interface for the actual three task scenarios.
      </b-card-text>

      <b-card-text>
        The <b> final </b> stage will then ask you some questions about your experience working with the system and doing the tasks.
      </b-card-text>

      <b-card-text>
        Upon completion of the seven stages, you can then switch back to Prolific to claim your payment.
      </b-card-text>

      <b-card-text>
        If you are happy to proceed, please enter your prolific id and click the <b> Agree and Continue </b> button below to start the task.
      </b-card-text>


      <b-card-text>
        This study is only compatible with desktops. Please do not take the study if you are using a tablet or a mobile phone, as this may result in your submission being rejected or returned.
      </b-card-text>





      <b-input-group>
        <template #prepend>
          <b-input-group-text variant="outline-info" class="email">{{emailBoxPrependText}}</b-input-group-text>
        </template>
        <b-form-input :placeholder="emailBoxPrependText" v-model="email" :state="isEmailValidState" />
      </b-input-group>

      <b-button class="mt-2" align-h="left" @click="agreeAndContinue()" variant="success">{{agreeButtonTxt}}</b-button>
      <template #footer>
<!--        <a href="https://www.flickr.com/photos/gerardstolk/49687926177" target="_blank">Image: CC BY-NC 2.0 by Gerard Stolk</a>-->
        <a href="https://thumbnails.production.thenounproject.com/G-t216xPxjp4fRL3iHisLx2nxj0=/fit-in/1000x1000/photos.production.thenounproject.com/photos/dark_camera_and_paper_on_world_map-scopio-27b68fe2-4a5f-46f3-a089-c948dc7985ff.jpg" target="_blank"></a>
      </template>
    </b-card>

  </b-container>
</template>

<script>

export default {
  name: "Introduction",
  data() {
    return {
      // todo refactor and remove unnecessary fields.
      training: false,
      prolific: String(import.meta.env.VITE_PROLIFIC).toLowerCase() === "true",
      baseUrl: String(import.meta.env.VITE_BACKEND_BASE_URL) + "/",
      email: undefined,
    }
  },
  methods: {
    agreeAndContinue: async function (){
      if (this.isValidEmail(this.email) || this.prolific){
        if(this.training)
          this.popupActivated = true;
        else
          await this.proceedToTask();
        return;
      }
      this.$vs.notify({
        title:'Invalid Email Address',
        text:'Please provide a valid email address',
        color:`rgb(72, 162, 211)`
      });
    },
    // todo refactor and remove this method.
    proceedToTask: async function (){
      const body = (this.prolific)? '{"prolific_id":"' + this.email + '"}' : '{"email":"' + this.email + '"}';
      const user_id = await this.getPreTest(body);

      let url = '/' + user_id + '/preTest';
      await this.$router.push(url);
    },
    // todo refactor and remove this method.
    isValidEmail: function (email) {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    // todo refactor and remove this method.
    async getPreTest(body) {
      try {
        // TODO call actual server
        // let response = await fetch(this.baseUrl + 'get_pre_test', {
        //   method: 'post',
        //   headers: {
        //     "Access-Control-Allow-Origin": "*",
        //     "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        //     "Content-Type": "application/json"
        //   },
        //   body: body
        // });

        let response = {
          json: async function (prolific){
            return (prolific)? JSON.parse(body).prolific_id: JSON.parse(body).email;
          }
        };

        // TODO remove prolific
        const user_id = await response.json(this.prolific)
        this.saveUserProgress(user_id);
        this.saveUserTasks(user_id);
        return user_id;
      } catch (error) {
        console.log(error);
      }
    },
    // todo rename tasks to something meaningful
    // todo remove this method
    saveUserTasks(user_id) {
      const data = {
        user_id: user_id
      }
      localStorage.setItem(user_id, JSON.stringify(data));
    },
    saveUserProgress: function (userId){
      localStorage.setItem(`${userId}-progress`, 'pretest');
    },
    failed: async function(){
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Failed',
        text: 'Unfortunately, you\'ve failed the quiz, it is not possible to continue the study!',
        accept:this.failed,
        close:this.failed,
        cancel:this.failed,
      })
    },
  },
  computed:{
    isEmailValidState: function (){
      if(this.prolific)
        return null;

      if (this.email) {
        return this.isValidEmail(this.email);
      }
      return null;
    },
    agreeButtonTxt: function (){
      return this.training ? "Agree and Continue to Tutorial" : "Agree and Continue";
    },
    emailBoxPrependText: function (){
      return (this.prolific) ? "Prolific ID" : "Email Address";
    }
  },
  mounted: async function() {
    const failed = localStorage.getItem('failed');
    if (failed === 'true'){
      await this.failed();
      return;
    }
    localStorage.clear();
  }
}
</script>

<style scoped>
.email{
  background-color: rgb(72, 162, 211);
  color: white;
}

.card{
  max-width: 70rem;
  margin-top: 0px;
  left:3%;
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card img{
  object-fit: cover;
}

.container{
  text-align: left;
  margin-top: 30px;
  width: 100%;
  border: none;
}
</style>