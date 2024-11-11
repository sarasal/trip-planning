<script setup>
import ProgressBar from '../components/ProgressBar.vue'
import Clock from '../components/Clock.vue'
import GeneralInfoCard from '../components/test/GeneralInfoCard.vue'
</script>

<template>
  <div v-if="finishedLoaded">
    <b-container style="min-width: 100%">
      <b-row v-if="!tutorial && !training" align-h="end" class="pb-1">
        <b-col cols="2">
            <b-pagination
                v-model="currentSample"
                :total-rows="6"
                :per-page="1"
                first-number
                last-number
                v-if="demoTab"
                size="sm"
                @page-click="nextSample"
            ></b-pagination>
        </b-col>
        <b-col v-if="progressBarSize === 7">
          <b-button v-if="demoTab" style="top: 0; font-size: 13px; padding: 4px 8px 4px;" @click="nextTab()" pill variant="outline-success">Next Tab</b-button>
        </b-col>
        <b-col :cols="progressBarSize" ref="progressBar" class="pr-1 pl-0">
          <ProgressBar v-if="!mainTasks" :max="3" :value="1" />
          <ProgressBar v-if="mainTasks" :max="this.user_tasks.length" :value="this.current_task_index" />
        </b-col>
        <b-col cols="1">
        </b-col>
        <b-col cols="1" ref="clock">
          <Clock v-if="userId" :paused="false" :user-id="userId" />
        </b-col>
      </b-row>
      <b-row v-if="!tutorial">
        <b-card>
          <div ref="scenario" style="font-size: 14px;margin-bottom: 20px" >
            <span v-html="current_task.scenario"></span>
          </div>
          <b-button
              v-if="mainTasks && !readMe"
              :class="!readMe ? null : 'collapsed'"
              :aria-expanded="!readMe ? 'true' : 'false'"
              aria-controls="collapse-1"
              variant="primary"
              @click="readMe = true">I read the text</b-button>
        </b-card>
      </b-row>
      <b-collapse id="collapse-1" v-model="readMe" class="mt-2">
      <b-row>
        <b-col cols="6" class="pr-0 pl-0">
          <b-row>
            <b-embed
                ref="map"
                type="iframe"
                aspect="16by9"
                :src="this.map_url"
                allowfullscreen
                v-on:load="mapLoaded()"
                @mouseover="hover.map = true"
                @mouseleave="hover.map = false"
            ></b-embed>
          </b-row>
          <b-row ref="mapControlPanel">
            <b-row>
              <b-pagination
                v-model="userFriendlyRouteIndex"
                :total-rows="route_info_list.length"
                :per-page="1"
                :limit="route_info_list.length"
                :hide-goto-end-buttons="true"
                align="fill"
                @change="routeChanged"
              ></b-pagination>
            </b-row>
            <b-row>
              <span style="padding-top: 5px">{{ route_name }}</span>
            </b-row>
          </b-row>
        </b-col>
        <b-col cols="2" id="myTestRef" ref="routeInfo" class="pr-0 pl-0" @mouseover="hover.routeInfo = true" @mouseleave="hover.routeInfo = false">
          <b-row v-if="this.route_start_time.length !== 0" style="margin-left: 15%; font-size: 12px; font-weight: bold;">Start time: {{this.route_start_time[this.current_route_index]}}</b-row>
          <b-row style="font-size: 12px" v-for="(subRoute, index) in this.current_route" :key="subRoute.sub_route_name">
            <b-col cols="1">
              <div class="my-icon" ref="transportMode">
                <b-iconstack>
                  <b-icon  icon="info-circle-fill" scale="3" :style="`color: ${route_info_styles[index].color}`"></b-icon>
                  <b-icon  icon="info-circle" scale="3" :style="`color: ${route_info_styles[index].color}`"></b-icon>
                </b-iconstack>
                <vs-icon class="transport-icon" :icon="route_info_styles[index].icon" round color="#ffffff"></vs-icon>
              </div>
              <div class="vertical-line" :style="`border-left: 4px dashed ${route_info_styles[index].color}`"></div>
            </b-col>
            <b-col>
            <b-row ref="subRouteName" style="margin-top: 5%;padding-bottom: 0;">
              {{ subRoute.sub_route_name }}
            </b-row>
            <b-row ref="capacityLevel" v-if="subRoute.capacity_level !== ''" :style="`color: ${route_info_styles[index].capacityLevelColor};padding-bottom: 0;`">
              {{capacityLevelText(subRoute.capacity_level)}}
            </b-row>
            <b-row ref="estimatedDuration" style="margin-button: 0;padding-bottom: 0;">
              Sub-Route Base Time : {{ minimumTime(subRoute) }} minutes
            </b-row>
            <b-row ref="fareCost" style="margin-button: 0;padding-bottom: 0;">
              Sub-Route Base Cost: {{ fareCost(subRoute) }}
            </b-row>
            </b-col>
          </b-row>
          <b-row style="font-size: 12px">
            <b-col cols="1">
              <div class="my-icon">
                <b-iconstack>
                  <b-icon  icon="info-circle-fill" scale="3" :style="`color: ${route_info_styles[route_info_styles.length-1].color}`"></b-icon>
                  <b-icon  icon="info-circle" scale="3" :style="`color: ${route_info_styles[route_info_styles.length-1].color}`"></b-icon>
                </b-iconstack>
                <vs-icon class="transport-icon" icon="location_on" round color="#ffffff"></vs-icon>
              </div>
            </b-col>
          </b-row>
        </b-col>
        <b-col cols="4" class="pr-0 pl-0">
          <div ref="generalInfo" @mouseover="hover.generalInfo = true" @mouseleave="hover.generalInfo = false">
            <GeneralInfoCard
                             :chance_list="chance_list"
                             :static_info="static_info"
                             :task_type="current_task.task_type"
                             :complexity="current_task.complexity"
                             :n_transfer="current_task.n_transfer"
            ></GeneralInfoCard>
          </div>
        </b-col>
      </b-row>

      <b-row v-if="!tutorial">

        <b-card style="width:100%; padding: 0" no-body ref="decisions">
          <template #header>
            <h1 style="font-size: 28px">Initial Decision</h1>
          </template>

          <div class="no-padding">
            <b-input-group v-if="initialDecision.enabled">

              <template #prepend>
                <b-input-group-text >What is the best plan in terms of minimising commute time and cost?</b-input-group-text>
              </template>

              <b-form-select v-model="initialDecision.value" :options="route_options">
                <template #first>
                  <b-form-select-option :value="null" disabled>Choose a route</b-form-select-option>
                </template>

              </b-form-select>

              <template #append>
                <b-button @click="submitInitialDecision()" ref="submitButton">submit</b-button>
              </template>
            </b-input-group>

            <b-text v-if="!initialDecision.enabled">
              You initially selected <span style="background-color: yellow;">{{initialDecision.value}}</span> as the best plan.
            </b-text>
          </div>
        </b-card>

        <b-card v-if="!initialDecision.enabled" style="width:100%; padding: 0; margin-top: 1rem; margin-bottom: 1rem">
          <template #header>
            <h1 style="font-size: 28px">AI Suggestion</h1>
          </template>
          <b-text>
            AI suggests that the <span style="background-color: yellow;">{{`Route ${Number(this.current_task.ai_route_id) +1}`}}</span> minimizes the commute time and cost.
          </b-text>
        </b-card>

        <b-card v-if="!initialDecision.enabled" style="width:100%; padding: 0;">
          <template #header>
            <h1 style="font-size: 28px">Final decision</h1>
          </template>

          <div class="no-padding">
            <b-input-group>

              <template #prepend>
                <b-input-group-text >What is the best plan in terms of minimising commute time and cost?</b-input-group-text>
              </template>

              <b-form-select v-model="finalDecision" :options="route_options">
                <template #first>
                  <b-form-select-option :value="null" disabled>Choose a route</b-form-select-option>
                </template>

              </b-form-select>

              <template #append>
                <b-button @click="submitFinalDecision()">submit</b-button>
              </template>
            </b-input-group>
          </div>

        </b-card>

      </b-row>
      </b-collapse>
    </b-container>
  </div>
</template>

<script>
import "intro.js/minified/introjs.min.css";
import introJS from 'intro.js';
import sample1 from '../samples/sample_tasks_1.json';
import sample2 from '../samples/sample_tasks_2.json';
import sample3 from '../samples/sample_tasks_3.json';
import sample4 from '../samples/sample_tasks_4.json';
import sample5 from '../samples/sample_tasks_5.json';
import sample6 from '../samples/sample_tasks_6.json';

const samples = [sample1,sample2,sample3,sample4,sample5,sample6];
const transportMap = {
  train: {
    icon: "train",
    color: "#4361ee",
  },
  taxi: {
    icon: "local_taxi",
    color: "#7b2cbf",
  },
  bus: {
    icon: "directions_bus",
    color: "#61a5c2",
  }
};

const capacityLevelMap = {
  green: {
    text: "Seats Available",
    color: "#1D931DFF",
  },
  orange: {
    text: "Limited Seats",
    color: "#ffa500",
  },
  red: {
    text: "No Seats",
    color: "#dc0c0c",
  },
};

export default {
  name: "Test",
  props: {
    onBoarding: {
      type: Boolean,
      default: false,
    },
    demoTab: {
      type: Boolean,
      default: false,
    },
    demoSession: {
      type: Boolean,
      default: false,
    },
    tutorial: {
      type: Boolean,
      default: false,
    },
    training: {
      type: Boolean,
      default: false,
    },
    mainTasks: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      finishedLoaded: false,
      currentSample: 1,
      readMe: !this.mainTasks,
      current_task_index: 0,
      userFriendlyRouteIndex: 1,
      current_route_index: 0,
      initialDecision: {
        enabled: true,
        value: "",
        timestamp: 0,
      },
      finalDecision: "",
      route_info_styles:[],
      userId: null,
      user_tasks: null,
      route_options: [],
      studyCondition: null,
      result: {
        user_id: null,
        study_condition: null,
        start_time: null,
        end_time: null,
        user_study: [],
        decision_times: [],
      },
      hover:{
        map: false,
        generalInfo: false,
        routeInfo: false,
      }
    }
  },
  methods: {
    nextTab: function () {
      this.$emit('nextTab');
    },
    nextSample: function (bvEvent, page){
      this.user_tasks = samples[page-1];
      this.regenerate_route_info_style();
      this.finalDecision = "";
      this.initialDecision = {
        enabled: true,
        value: "",
        timestamp: 0,
      }
    },
    routeChanged: function (page) {
      this.emitBackendEvent('CLICK', this.getCurrentTimestamp(), (page-1));
      this.current_route_index = page -1;
      this.regenerate_route_info_style();
    },
    regenerate_route_info_style: function (){
      const styles = []
      let transport, capacityLevel, capacityLevelColor;
      for(let i=0; i<this.current_route.length; i++){
        transport = this.current_route[i].transport;
        capacityLevel = this.current_route[i].capacity_level;
        capacityLevelColor = (capacityLevel === '')? '' : capacityLevelMap[capacityLevel].color;
        styles.push({
          color: transportMap[transport].color,
          icon: transportMap[transport].icon,
          capacityLevelColor: capacityLevelColor,
        })
      }
      this.route_info_styles = styles
    },
    roundNumber: function ( number , precision) {
      let numberStr = number.toString();
      let dotPosition = numberStr.indexOf('.')
      return numberStr.slice(0, (dotPosition + 1) + precision)
    },
    fareCost: function (subRoute) {
      const transport = subRoute.transport
      const length = subRoute.length
      const costFares = this.static_info[0]
      if((costFares[transport] * length) < 0.01){
        return "0.01 €"
      }
      return `${this.roundNumber((costFares[transport] * length), 2)} €`;
      // return `${(costFares[transport] * length)/1000} €`;
    },
    minimumTime: function (subRoute) {
      if (subRoute === undefined)
        return "";

      // if (subRoute.transport === 'train') {
      //   if(this.current_task.task_type !== "diagnostic") {
      //     return this.roundNumber(subRoute.duration_range[0], 1);
      //   }
      //   return this.roundNumber(subRoute.duration, 1);
      // }
      
      // if (subRoute.duration.toString() !== "0") {
      //   return this.roundNumber(subRoute.duration, 1);
      // }

      if (subRoute.duration_range.length === 0) {
        if(subRoute.duration === 0){
          return "0.1"
        }
        return this.roundNumber(subRoute.duration, 1);
      }

      if(subRoute.duration_range[0]===0 && subRoute.duration_range[1]===0){
        return "0.0 - 0.1"
      }
      return  `${this.roundNumber(subRoute.duration_range[0], 1)} - ${this.roundNumber(subRoute.duration_range[1], 1)}`;
    },
    submitInitialDecision: function (){
      if(this.initialDecision.value === ""){
        this.$vs.notify({
          title:'Empty Initial Decision',
          text:'You didn\'t make your initial decision. Please identify your choice and then click on submit.',
          color:`rgb(211,72,93)`
        });
        return;
      }
      this.initialDecision.timestamp = this.getCurrentTimestamp();
      this.initialDecision.enabled = false;
      this.emitBackendEvent('INITIAL_SUBMISSION', this.initialDecision.timestamp, this.routeNameToIndex(this.initialDecision.value));
    },
    routeNameToIndex: function (name){
      return `${parseInt(name.replace('Route ', '')) -1}`;
    },
    submitFinalDecision: async function (){
      if(this.finalDecision === ""){
        this.$vs.notify({
          title:'Empty Final Decision',
          text:'You didn\'t make your final decision. Please identify your choice and then click on submit.',
          color:`rgb(211,72,93)`
        });
        return;
      }

      const finalSubmissionTimestamp = this.getCurrentTimestamp();

      this.result.user_study.push({
        task_id: this.current_task.task_id,
        initial_decision: this.routeNameToIndex(this.initialDecision.value),
        final_decision: this.routeNameToIndex(this.finalDecision),
      });

      this.emitBackendEvent('FINAL_SUBMISSION', finalSubmissionTimestamp, this.routeNameToIndex(this.finalDecision));

      this.result.decision_times.push({
        task_id: this.current_task.task_id,
        start_decision: this.initialDecision.timestamp,
        end_decision: finalSubmissionTimestamp,
      });

      if(this.training){
        this.$emit('trainingFinished');
        return;
      }

      if(this.current_task_index === this.user_tasks.length -1) {
        this.result.end_time = finalSubmissionTimestamp;
        const res = await this.updateBackend('submit_user_study', this.result);
        localStorage.setItem(`${this.userId}-score`, res.score);
        this.$emit('mainTasksFinished');
        return;
      }

      this.finalDecision = "";
      this.initialDecision = {
        enabled: true,
        value: "",
        timestamp: 0,
      }
      this.current_task_index++;
      this.current_route_index=0;
      this.userFriendlyRouteIndex=1;
      this.readMe = false;
    },
    emitBackendEvent: function (type, timestamp, value){
      if (!this.mainTasks){
        return;
      }

      const body = {
        user_id: this.userId,
        study_condition: `${this.studyCondition}`,
        task_id: this.current_task.task_id,
        event_type: type,
        timestamp: `${timestamp}`,
        event_value: `${value}`
      };

      this.updateBackend('submit_event', body);
    },
    updateBackend: async function (url, newBody){
      const rawBody = {
        "user_id": this.userId,
        "study_condition": this.studyCondition,
      };

      const body = (newBody === undefined)? rawBody: newBody;

      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
      };

      const res = await fetch(`${window.location.origin}/api/${url}`, requestOptions);
      if (url !== 'submit_event'){
        return await res.json();
      }
    },
    capacityLevelText: function (capacityLevel){
      return capacityLevelMap[capacityLevel].text;
    },
    getCurrentTimestamp: function () {
      return Date.now();
    },
    mapLoaded: function (){

      if (!this.tutorial && !this.onBoarding){
        return
      }

      if(this.onBoarding){
        this.run_introJS();
        return;
      }


      const task = this;
      const intro = introJS()
      let finished = false;

      intro.oncomplete(function () {
        task.$emit('tutorialFinished');
        finished = true;
        intro.exit(true);
      });

      // console.log("inside on load");
      // In Chrome console use:
      // document.getElementById('my_map_1191').contentWindow.document.getElementById('tooltip_13748ca0330647a2b0314a22ebc069ae')
      // const el = this.$refs.map.firstChild.contentWindow.document.getElementById('html_8bfdd3523d246ca66b7ff7e4b254b1a8');
      // const el2 = this.$refs.myTestRef;
      // console.log(el2)

      // intro.addStep({
      //   element: el,
      //   intro: "Ok, wasn't that fun?",
      //   position: 'right'
      // });
      // this.intro.addStep({
      //   element: el2,
      //   intro: "Ok, wasn't that fun?",
      //   position: 'right'
      // });

      // todo use this trick to access child
      // console.log(this.$refs.generalInfo.children);
      const generalInfoRefs = this.$refs.generalInfo.children[0].__vue__.$refs;
      const transportFareEl = generalInfoRefs.costCard.$refs.transportFare.$el;

      let subscriptionEl, rainEl, trafficEl, capacityLevel, capacityEl, peakFaresEl, peakFares, distanceBasedDiscount, distanceBasedDiscountEl, limitedTransfersEl, stopEL;


      if (this.studyCondition >= 3 ){
        subscriptionEl = generalInfoRefs.costCard.$refs.subscription.$el;
        capacityLevel = this.$refs.capacityLevel[0];
      }


      if(this.studyCondition === 4 || this.studyCondition === 6){

        // rain
        if(parseInt(this.chance_list[0]['chance']) >= 60){
          rainEl = generalInfoRefs.rainHigh;
        }
        if(parseInt(this.chance_list[0]['chance']) < 60){
          rainEl = generalInfoRefs.rainLow;
        }


        // traffic
        if(parseInt(this.chance_list[1]['chance']) >= 60){
          trafficEl = generalInfoRefs.trafficHigh;
        }

        if(parseInt(this.chance_list[1]['chance']) < 60){
          trafficEl = generalInfoRefs.trafficLow;
        }


        // capacity
        if(parseInt(this.chance_list[2]['chance']) >= 60){
          capacityEl = generalInfoRefs.capacityHigh;
        }

        if(parseInt(this.chance_list[2]['chance']) < 60){
          capacityEl = generalInfoRefs.capacityLow;
        }


        // pick-up point
        if(parseInt(this.chance_list[3]['chance']) >= 60){
          stopEL = generalInfoRefs.stopHigh;
        }

        if(parseInt(this.chance_list[3]['chance']) < 60){
          stopEL = generalInfoRefs.stopLow;
        }

      }



      if(this.studyCondition === 3 || this.studyCondition === 5){
        rainEl = generalInfoRefs.rainFixed;
        capacityEl = generalInfoRefs.capacityFixed;
        trafficEl = generalInfoRefs.trafficFixed;
      }

      if(this.studyCondition === 5){
        stopEL = generalInfoRefs.stopFixed;
      }

      // peak fares, distance-based discount, limited transfers
      if (this.studyCondition >= 5 ){
        peakFaresEl = generalInfoRefs.peakFares;
        peakFares = generalInfoRefs.costCard.$refs.peakFare.$el;

        distanceBasedDiscountEl = generalInfoRefs.distantBasedFare;
        distanceBasedDiscount = generalInfoRefs.costCard.$refs.distanceBasedDiscount.$el;
        limitedTransfersEl = generalInfoRefs.limitedTransfers;
      }


      const steps = [
        {
          title: 'welcome',
          intro: 'This is the task tutorial to understand the different factors that can impact travel times and cost for commuters. Click on the next button to start.',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.map,
          intro: "The name of each sub-route.",
          position: 'right',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.subRouteName[0],
          intro: "The name of each sub-route.",
          position: 'right',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.map,
          intro: "The mode of transportation includes a train, taxi, and bus. Each sub-route is indicated by a distinct logo to identify it.",
          position: 'bottom',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.transportMode[0],
          intro: "The transportation mode is also displayed here.",
          position: 'right',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: transportFareEl,
          intro: "The cost of each transportation mode per kilometer in Euro.",
          position: 'left',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.fareCost[0],
          intro: "The base cost for each sub-route is determined by multiplying the distance of this sub-route by its corresponding public transport fare per kilometer.",
          position: 'right',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.map,
          intro: "The shortest time it would take to travel along this sub-route, based solely on the distance and speed of public transportation.",
          position: 'right',
          studyConditions: [1,3,5],
        },
        {
          element: this.$refs.estimatedDuration[0],
          intro: "The shortest time is also displayed here.",
          position: 'right',
          studyConditions: [1,3,5],
        },
        {
          element: this.$refs.map,
          intro: "The range of shortest time it would take to travel along this sub-route, based solely on the distance and speed of public transportation.",
          position: 'right',
          studyConditions: [2,4,6],
        },
        {
          element: this.$refs.estimatedDuration[0],
          intro: "The range of shortest time is also displayed here.",
          position: 'right',
          studyConditions: [2,4,6],
        },
        {
          element: this.$refs.map,
          intro: "The length of each sub-route is presented in kilometers.",
          position: 'right',
          studyConditions: [1,2,3,4,5,6],
        },
        {
          element: this.$refs.map,
          intro: "The seat availability on the train or bus is displayed. In situations where no or limited seats are available, there is a possibility of not catching the intended bus or train, resulting in an additional travel time of 10 (for buses) to 20 minutes (for trains).",
          position: 'top',
          studyConditions: [3,4,5,6],
        },
        {
          element: capacityLevel,
          intro: "The seat availability on the train or bus is also displayed here.",
          position: 'top',
          studyConditions: [3,4,5,6],
        },
        {
          element: capacityEl,
          intro: "The seat availability on the train or bus is also described here.",
          position: 'left',
          studyConditions: [3,4,5,6],
        },
        {
          element: rainEl,
          intro: "Today is rainy. Rain slows down buses and taxi’s, leading to longer commute times by around 40%.",
          position: 'left',
          studyConditions: [3,5],
        },
        {
          element: rainEl,
          intro: "There is a chance of rain. Rain slows down buses and taxi’s, leading to longer commute times by around 40%.",
          position: 'left',
          studyConditions: [4,6],
        },
        {
          element: this.$refs.map,
          intro: "The traffic conditions are classified as normal, moderate, or heavy depending on the level of congestion. When the traffic is determined to be moderate or heavy, the corresponding sub-route will appear in orange or red colors which indicate potential delays for taxis and buses thereby increasing their travel time.",
          position: 'left',
          studyConditions: [3,4,5,6],
        },
        {
          element: trafficEl,
          intro: "The traffic jam is also described here.",
          position: 'left',
          studyConditions: [3,4,5,6],
        },
        {
          element: subscriptionEl,
          intro: "By having a subscription to both taxi and bus services, the passenger is able to enjoy reduced fares at a fixed rate.",
          position: 'left',
          studyConditions: [3,4,5,6],
        },
        {
          element: peakFares,
          intro: "During peak-hour periods, the fare cost is subject to a percentage increase per kilometer traveled.",
          position: 'left',
          studyConditions: [5,6],
        },
        {
          element: peakFaresEl,
          intro: "Peak-hour periods are defined here.",
          position: 'left',
          studyConditions: [5,6],
        },
        {
          element: distanceBasedDiscount,
          intro: "Passengers can receive a percentage discount on their fare when they exceed a certain distance travelled.",
          position: 'left',
          studyConditions: [5,6],
        },
        {
          element: distanceBasedDiscountEl,
          intro: "Kilometer-based discount is also described here.",
          position: 'left',
          studyConditions: [5,6],
        },
        {
          element: limitedTransfersEl,
          intro: "It is highly recommended for passengers to restrict the number of transfers they make during their trip.",
          position: 'left',
          studyConditions: [5,6],
        },
        {
          element: this.$refs.map,
          intro: "The passengers need to collect an item from a specific place during their travel.",
          position: 'left',
          studyConditions: [5],
        },
        {
          element: this.$refs.map,
          intro: "There is a possibility that passengers may need to collect an item from a specific place during their travel. The likelihood of this feature appearing has been estimated at a certain percentage.",
          position: 'left',
          studyConditions: [6],
        },
        {
          element: stopEL,
          intro: "The requirement to cross the certain point is also described here.",
          position: 'left',
          studyConditions: [5, 6],
        },
        {
          title: 'congratulation',
          intro: 'You have acquired the necessary knowledge to complete this study. Click on the Done button to demonstrate your newfound skills by carrying out a sample task.',
          studyConditions: [1,2,3,4,5,6],
        },
      ];

      intro.addSteps(steps.filter(step => step.studyConditions.indexOf(task.studyCondition)>=0));

      intro.setOptions({
        'disableInteraction': true,
        'exitOnOverlayClick': false,
        'exitOnEsc': false
      });

      intro.onbeforeexit(function() {
        if(task.demoSession){
          task.$emit('tutorialFinished');
          return true;
        }
        if(!finished) {
          task.$vs.notify({
            title: 'It is not possible to exit',
            text: 'Please follow all the steps',
            color: `rgb(255, 165, 0)`
          });
          return false;
        }
      });

      intro.start();
    },
    run_introJS: function () {
      const task = this;
      let finished = false;

      const intro = introJS()

      intro.oncomplete(function () {
        task.$emit('onBoardingFinished');
        finished = true;
        intro.exit(true);
      });

      const steps = [
        {
          title: 'welcome',
          intro: 'This is the interface tutorial to get to know the different components on the screen. Click on the next button to start.'
        },
        {
          element: this.$refs.scenario,
          intro: "Please take a minute to read your task description. Note that you do not have to memorize the task description.",
          position: 'bottom'
        },
        {
          element: this.$refs.map,
          intro: "For each route, the details of the commute plan are presented on the map. Their colors distinguish sub-routes. You can click on each sub-route to see more information. You can hover over the sub-route to show its name.",
          position: 'right'
        },
        {
          element: this.$refs.mapControlPanel,
          intro: "You can use these buttons to change the highlighted route on the map.",
          position: 'top'
        },
        {
          element: this.$refs.routeInfo,
          intro: "You can also see the details of the commute plan for the highlighted route here.",
          position: 'right'
        },
        {
          element: this.$refs.generalInfo,
          intro: "You can view available information regarding all routes.",
          position: 'left'
        },
        {
          element: this.$refs.decisions,
          intro: "You should answer this question twice. After you make the initial decision, the AI suggestion is shown. You can then submit your final decision.",
          position: 'top'
        },
        {
          element: this.$refs.progressBar,
          intro: "You can view the progress here.",
          position: 'bottom'
        },
        {
          element: this.$refs.clock,
          intro: "The timer starts when you enter the main study.",
          position: 'left'
        },
        {
          title: 'congratulation',
          intro: 'By now, you should be acquainted with the elements displayed on your screen. To deep dive into a tutorial on utilizing the study\'s task features, simply click on the Done button.'
        },
      ];

      intro.addSteps(steps);

      intro.setOptions({
        'disableInteraction': true,
        'exitOnOverlayClick': false,
        'exitOnEsc': false
      });

      intro.onbeforeexit(function() {
        if(task.demoSession){
          task.$emit('onBoardingFinished');
          return true;
        }

        if(!finished){
          task.$vs.notify({
            title:'It is not possible to exit',
            text:'Please follow all the steps',
            color:`rgb(255, 165, 0)`
          });
          return false;
        }
      });

      intro.start();
    },
    generate_route_options: function () {
      let options = [];
      for (let i = 0; i < this.route_info_list.length; i++) {
        options.push(`Route ${i+1}`)
      }
      return options
    },
  },
  watch:{
    'hover.map'(newValue){
      const type = (newValue)? 'HOVER_IN' : 'HOVER_OUT';
      this.emitBackendEvent(type, this.getCurrentTimestamp(), 'map');
    },
    'hover.routeInfo'(newValue){
      const type = (newValue)? 'HOVER_IN' : 'HOVER_OUT';
      this.emitBackendEvent(type, this.getCurrentTimestamp(), 'route_information');
    },
    'hover.generalInfo'(newValue){
      const type = (newValue)? 'HOVER_IN' : 'HOVER_OUT';
      this.emitBackendEvent(type, this.getCurrentTimestamp(), 'general_information');
    },
  },
  computed: {
    current_task: function () {
      return this.user_tasks != null ? this.user_tasks[this.current_task_index] : {};
    },
    map_url: function () {
      if(this.tutorial && this.current_route_index === 0){ // todo remove this if
        return this.user_tasks != null ? `${window.location.origin}/maps/task_${this.current_task.task_id}_route0_tutorial.html` : "";
      }
      return this.user_tasks != null ? `${window.location.origin}/maps/task_${this.current_task.task_id}_route${this.current_route_index}.html` : "";
    },
    route_info_list: function () {
      return this.user_tasks != null ? JSON.parse(this.user_tasks[this.current_task_index].route_info_list.replace(/'/g, '"')) : [];
    },
    route_start_time: function () {
      return this.user_tasks != null ? JSON.parse(this.user_tasks[this.current_task_index].route_start_time.replace(/'/g, '"')) : [];
    },
    static_info: function (){
      return this.user_tasks != null ? JSON.parse(this.user_tasks[this.current_task_index].static_info.replace(/'/g, '"')) : [];
    },
    chance_list: function (){
      return this.user_tasks != null ? JSON.parse(this.user_tasks[this.current_task_index].chance_list.replace(/'/g, '"')) : [];
    },
    current_route: function () {
      return this.user_tasks != null ? this.route_info_list[this.current_route_index].route : {};
    },
    route_name: function () {
      return `Route ${this.userFriendlyRouteIndex}`
    },
    progressBarSize: function () {
      return (this.demoTab)? 7 : 8;
    }
  },
  created: async function() {
    if(this.demoTab){
      this.user_tasks = sample1;
    }

    this.userId =  this.$route.params.userId;
    this.studyCondition = parseInt(JSON.parse(localStorage.getItem(`${this.userId}-info`)).study_condition);

    if (this.training || this.tutorial || this.onBoarding){
      const res = await this.updateBackend('get_user_training_task');
      this.user_tasks = [res]
    }

    if (this.mainTasks){
      this.result.user_id = this.userId;
      this.result.study_condition = this.studyCondition;
      this.result.start_time = this.getCurrentTimestamp();
      this.user_tasks = await this.updateBackend('get_user_task_instances');
    }

    this.route_options = this.generate_route_options();
    this.regenerate_route_info_style();
    this.finishedLoaded=true;
  },
}
</script>

<style scoped>
div {
  padding: 5px;
  margin: 0px;
}

.progress-bar {
  min-height: 10%;
}

.vertical-line {
  border-left: 4px dashed #1d931d;
  display: block;
  height: 100%;
  position: absolute;
  margin-left: 10px;
  margin-right: 5px;
}

.transport-icon {
  z-index: 10;
  position: absolute;
  margin-left: -88%;
  margin-top: -21%;
}

.my-icon {
  z-index: 9;
  position: absolute;
  margin-left: 15%;
  margin-top: -50%;
}

.no-padding {
  padding: 1rem;
}

.no-padding >>> div{
  padding: 0;
}
</style>