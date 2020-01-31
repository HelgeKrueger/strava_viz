<template>
  <div>
    <p>Hello</p>
    <router-link to="/">Welcome</router-link>
    <router-link to="/calendar">Calendar</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
import Vue from "vue";
import Router from "vue-router";

import Calendar from "./Calendar.vue";
import Welcome from "./Welcome.vue";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "Welcome",
      component: Welcome
    },
    {
      path: "/calendar",
      name: "Calendar",
      component: Calendar
    }
  ]
});

export default {
  name: "App",
  router: router,
  components: {
    Calendar,
    Welcome
  }
};
</script>

<style></style>
