// src/components/Header.vue
<template>
  <header class="app-header">
    <div class="header-left">
      <Logo @click="goHome" />
    </div>
    <Menubar :model="items" class="nav-menubar"></Menubar>
    <Button @click="goLogin" label="Login" icon="pi pi-user" class="p-button-outlined p-button-secondary login-button" />
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import Menubar from 'primevue/menubar';
import Button from 'primevue/button';
import Logo from './Logo.vue';

const router = useRouter();

const items = [
  {
    label: 'Home',
    icon: 'pi pi-fw pi-home',
    command: () => { router.push('/'); }
  },
  {
    label: 'Debug',
    icon: 'pi pi-fw pi-cog',
    command: () => { router.push('/debug'); }
  },
  {
    label: 'Dictionary',
    icon: 'pi pi-fw pi-book',
    command: () => { router.push('/dictionary'); }
  }
];

function goHome() {
  router.push('/');
}

function goLogin() {
  router.push('/login');
}
</script>

<style scoped>
.app-header {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  background-color: #333;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5em 1rem;
}

.header-left {
  display: flex;
  align-items: center;
}

.nav-menubar {
  flex-grow: 1;
  background-color: #333;
  border: none;
  display: flex;
  justify-content: center;
}

.nav-menubar .p-menubar-root-list {
  display: flex;
  justify-content: center;
  flex-grow: 1;
}

.nav-menubar .p-menuitem {
  margin: 0 1rem;
}

.app-header .p-menuitem-link {
  color: white;
  font-weight: bold;
}

.app-header .p-menuitem-link:hover {
  color: #ffcc00;
}

.login-button {
  margin-left: auto;
}

.p-button {
  left: 0;
}
</style>
