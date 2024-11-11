<template>
  <span class="time">
    {{ time }}

    <b-icon @click="pauseTask()"
            v-if="pauseEnabled"
            icon="pause"
            font-scale="1.2"
            scale="2"
            class="bg-info p-1"
            variant="light" ></b-icon>
  </span>
</template>

<script>
// todo move these to shared
function zeroPrefix(num, digit) {
  let zero = '';
  for(let i = 0; i < digit; i++) {
    zero += '0';
  }
  return (zero + num).slice(-digit);
}

function timeToString( time ){

  const hour = time.getUTCHours()
      , min = time.getUTCMinutes()
      , sec = time.getUTCSeconds()

  return zeroPrefix(hour, 2) + ":" +
  zeroPrefix(min, 2) + ":" +
  zeroPrefix(sec, 2);
}

export default {
  name: "Clock",
  props:{
    paused: Boolean,
    userId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      // pauseEnabled: String(process.env.VUE_APP_PAUSE).toLowerCase() === "true",
      pauseEnabled: false,
      timeBegan: new Date(),
      pauseTime: undefined,
      pauseDuration: undefined,
      time: '00:00:00'
    }
  },
  watch:{
    paused: function (){
      if (!this.paused) {
        const startTime = new Date,
            timeElapsed = new Date(startTime - this.pauseTime);

        if (this.pauseDuration !== undefined) {
          this.pauseDuration = new Date( this.pauseDuration.getTime() + timeElapsed.getTime());
        } else {
          this.pauseDuration = new Date( startTime - this.pauseTime);
        }
      }
    }
  },
  methods:{
    clockRunning: function () {
      if(this.paused)
        return;

      const currentTime = new Date();
      let timeElapsed = new Date(currentTime - this.timeBegan );


      if (this.pauseDuration !== undefined) {
        timeElapsed = new Date(timeElapsed - this.pauseDuration);
      }

      this.time = timeToString(timeElapsed);
    },
    pauseTask: function (){
      this.pauseTime = new Date();
      this.$emit('pauseTask', this.pauseTime);
    }
  },
  created: function (){
    const timeBegan = localStorage.getItem(this.userId + "timeBegan");

    if(!timeBegan)
      localStorage.setItem(this.userId + "timeBegan", this.timeBegan.toString());
    else
      this.timeBegan = Date.parse(timeBegan);

    setInterval(this.clockRunning, 10);
  }
}
</script>

<style scoped>
.time{
  order: 0;
  flex: 0 1 auto;
  float: right;
  align-self: center;
  color: rgb(41, 87, 201);
}
</style>