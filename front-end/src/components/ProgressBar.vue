<template>
  <b-progress :max="max" height="30px" animated>
    <b-progress-bar :value="value + finished" height="30px" variant="success" >
      <span>Answered: <strong>{{ value + finished}} / {{ max }}</strong></span>
    </b-progress-bar>
    <b-progress-bar :value="1-finished" variant="warning"></b-progress-bar>
  </b-progress>
</template>

<script>
export default {
  name: "ProgressBar",
  props:{
    max: {
      type: Number,
      required: true,
    },
    value: {
      type: Number,
      required: true
    },
    finished: {
      type: Number,
      required: false,
      default: 0,
    }
  },
}
</script>