<template>
  <div>
    <div class="navigation-menu">
      <router-link to="/">Welcome</router-link>
      <router-link to="/calendar">Calendar</router-link>
      <router-link to="/aggregated">Aggregated</router-link>
      <router-link to="/monthly">Monthly</router-link>
      <router-link to="/activitymap">Map</router-link>
      <span class="float-right">
        <UpdateData />
      </span>
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
import UpdateData from "./UpdateData.vue";
import ActivityMap from "./ActivityMap.vue";

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
  ].concat(buildRoutes([Calendar, Aggregated, Monthly, ActivityMap]))
});

export default {
  name: "App",
  router: router,
  components: {
    Calendar,
    Welcome,
    Aggregated,
    Monthly,
    UpdateData,
    Map
  },
  methods: {
    updateData: () => {}
  }
};
</script>

<style>
div.navigation-menu {
  background-color: darkblue;
  padding: 20px;
}

div.navigation-menu a {
  color: white;
}

div.navigation-menu a:visited {
  color: white;
}

div.navigation-menu .float-right {
  float: right;
}
</style>
