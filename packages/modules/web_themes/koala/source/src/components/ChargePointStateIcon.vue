<template>
  <q-icon
    :name="plugState ? 'power' : 'power_off'"
    size="sm"
    :color="plugState ? (chargeState ? 'positive' : 'warning') : 'negative'"
  >
    <q-tooltip>
      {{
        plugState
          ? chargeState
            ? 'Lädt'
            : 'Angesteckt, lädt nicht'
          : 'Nicht angesteckt'
      }}
    </q-tooltip>
  </q-icon>
</template>

<script setup lang="ts">
import { useMqttStore } from 'src/stores/mqtt-store';
import { computed } from 'vue';

const props = defineProps<{
  chargePointId: number;
}>();

const mqttStore = useMqttStore();

const plugState = computed(() =>
  mqttStore.chargePointPlugState(props.chargePointId),
);
const chargeState = computed(() =>
  mqttStore.chargePointChargeState(props.chargePointId),
);
</script>
