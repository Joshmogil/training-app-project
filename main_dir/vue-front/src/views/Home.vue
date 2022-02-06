<template>
  <div class="home">
    <h1>Home</h1>
    <p>You must be authenticated to see this</p>
    <div>{{$store.state.user.is_active}}</div>
  </div>
</template>

<script>
export default {
  name: "home"
};
</script>
