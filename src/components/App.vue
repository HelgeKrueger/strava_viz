<template>
  <div>
    <p>Hello</p>
    <router-link to="/">Welcome</router-link>
    <router-link to="/calendar">Calendar</router-link>
    <router-link to="/aggregated">Aggregated</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
import Vue from "vue";
import Router from "vue-router";

import Calendar from "./Calendar.vue";
import Welcome from "./Welcome.vue";
import Aggregated from "./Aggregated.vue";

Vue.use(Router);

console.log(Aggregated.name);

function buildRoutes(components) {
  return components.map(component => {
    const name = component.name;
    return {
      path: `/${name.toLowerCase()}`,
      name: name,
      component: component
    };
  });
}

const router = new Router({
  routes: [
    {
      path: "/",
      name: "Welcome",
      component: Welcome
    }
  ].concat(buildRoutes([Calendar, Aggregated]))
});

export default {
  name: "App",
  router: router,
  components: {
    Calendar,
    Welcome,
    Aggregated
  }
};
</script>

<style></style>
