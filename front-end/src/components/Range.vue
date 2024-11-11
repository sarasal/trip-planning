<template>
  <b-card :class="`my-card my-card-${this.bCardColor}-color`">
    <label class="bigger-txt" for="range-1">{{index+1}}. {{question}}</label>
    <b-row>
      <b-col class="no-padding" align="right" :cols="firstColumns">
        <label for="range-1" :class="`range-labels range-labels-${this.bCardColor}-color`">{{beginningLabel}}</label>
      </b-col>
      <b-col class="no-padding" :cols="10-firstColumns">
        <b-form-rating :class="`my-card-${this.bCardColor}-color`" icon-empty="circle" icon-full="circle-fill" v-model="selected" no-border :stars="max"></b-form-rating>
      </b-col>
      <b-col class="no-padding" cols="2" align="center">
        <label for="range-1" :class="`range-labels range-labels-${this.bCardColor}-color`">{{endLabel}}</label>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
export default {
  name: "Range",
  props:{
    question: {
      type: String,
      required: true
    },
    max: {
      type: Number,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    beginningLabel: {
      type: String,
      required: true
    },
    endLabel: {
      type: String,
      required: true
    },
    becomeRedIfEmpty: {
      type: Boolean,
      required: true
    },
  },
  data() {
    return {
      selected: '-1',
    }
  },
  computed: {
    firstColumns: function (){
      return (this.beginningLabel.length> 21) ? 3 : 2;
    },
    bCardColor: function (){
      if(this.becomeRedIfEmpty){
        if(this.selected === "-1" || this.selected === undefined){
          return "red"
        }
        return "green"
      }
      return "gray";
    }
  },
  watch:{
    selected: function (val){
      this.$emit('selectedChanged', {question: this.question, answer: val, type: 'Range', index: this.index});
    }
  },
}
</script>

<style scoped>

.no-padding  {
  padding: 5px;
}

.range-labels {

  border-radius: 30px;
  padding: 5px;
}

.range-labels-gray-color {
  border: 2px solid #959690FC;
  background: #c7c3c3;
}

.range-labels-red-color {
  border: 2px solid #940A0AA6;
  background: #CE0E0EA6;
}

.range-labels-green-color {
  border: 2px solid #18940AA6;
  background: #42AB35A5;
}

.my-card {
  padding: 0;
  margin-bottom: 2rem;
  border-radius: 30px;
}

.my-card-gray-color {
  border: 2px solid #959690FC;
  background: #faf7f7;
}

.my-card-red-color {
  border: 2px solid #940A0AA6;
  background: #D53333A5;
}

.my-card-green-color {
  border: 2px solid #18940AA6;
  background: #55D544A5;
}

.bigger-txt {
  font-size: 24px;
}
</style>