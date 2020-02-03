<template>
  <div>
    <a href="#" v-on:click="update" v-if="!updating">Update Data</a>
    <span v-if="updating">Updating</span>
  </div>
</template>

<script>
export default {
  name: "UpdateData",
  data: () => {
    return {
      updating: false
    };
  },
  methods: {
    update: function() {
      this.updating = true;

      fetch("/app/update_data")
        .then(data => data.json())
        .then(data => {
          console.log(data);
          setTimeout(() => {
            this.updating = false;
          }, 1000);
        });
    }
  }
};
</script>