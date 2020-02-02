<template>
  <div>
    <div class="navigation-menu">
      <router-link to="/">Welcome</router-link>
      <router-link to="/calendar">Calendar</router-link>
      <router-link to="/aggregated">Aggregated</router-link>
      <router-link to="/monthly">Monthly</router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import Vue from "vue";
import Router from "vue-router";

import Calendar from "./Calendar.vue";
import Welcome from "./Welcome.vue";
import Aggregated from "./Aggregated.vue";
import Monthly from "./Monthly.vue";

Vue.use(Router);

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
  ].concat(buildRoutes([Calendar, Aggregated, Monthly]))
});

export default {
  name: "App",
  router: router,
  components: {
    Calendar,
    Welcome,
    Aggregated,
    Monthly
  }
};
</script>

<style>
div.navigation-menu {
  background-color: darkblue;
  padding: 20px;
}

a {
  color: white;
}

a:visited {
  color: white;
}
</style>
