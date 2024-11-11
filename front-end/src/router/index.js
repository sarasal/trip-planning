import Vue from 'vue'
import VueRouter from 'vue-router'
import Introduction from '../views/Introduction.vue'
import PreTest from '../views/PreTest.vue'
import Test from '../views/Test.vue'
import MainWindow from '../views/MainWindow.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Introduction
    }, {
      path: '/:userId/preTest',
      alias: ['/:userId/demo', '/:userId/onBoarding', '/:userId/tutorial', '/:userId/training', '/:userId/quiz', '/:userId/mainTask', '/:userId/postTest', '/:userId/score'],
      name: 'MainWindow',
      component: MainWindow,
    }, {
      path: '*',
      redirect: '/'
    }
  ]
})

export default router
