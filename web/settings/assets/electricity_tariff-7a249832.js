import{_ as s,q as c,k as u,l as d,B as i,M as f,x as p}from"./vendor-b3afda6d.js";import"./vendor-sortablejs-806a0b5c.js";const _={name:"ElectricityTariffRabot",emits:["update:configuration"],props:{electricityTariff:{type:Object,required:!0}},data(){return{}},methods:{updateConfiguration(n,e=void 0){this.$emit("update:configuration",{value:n,object:e})}}},b={class:"electricity-tariff-rabot"};function m(n,e,a,g,y,r){const l=c("openwb-base-alert"),o=c("openwb-base-text-input");return u(),d("div",b,[i(l,{subtype:"info"},{default:f(()=>[p(" Ihre persönlichen Zugangsdaten (Client-ID und Client-Secret) erhalten Sie direkt von Rabot. Behandeln Sie diese Daten wie ein Passwort, da sich darüber auch persönliche Daten aus Ihrem Rabot-Account abfragen lassen! ")]),_:1}),i(o,{title:"Client-ID",subtype:"user",required:"","model-value":a.electricityTariff.configuration.client_id,"onUpdate:modelValue":e[0]||(e[0]=t=>r.updateConfiguration(t,"configuration.client_id"))},null,8,["model-value"]),i(o,{title:"Client-Secret",subtype:"password",required:"","model-value":a.electricityTariff.configuration.client_secret,"onUpdate:modelValue":e[1]||(e[1]=t=>r.updateConfiguration(t,"configuration.client_secret"))},null,8,["model-value"])])}const w=s(_,[["render",m],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/electricity_tariffs/rabot/electricity_tariff.vue"]]);export{w as default};