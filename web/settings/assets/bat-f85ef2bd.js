import{_ as u,q as c,l as _,m,A as n,K as o,v as t,u as e,x as l}from"./vendor-29588c66.js";import"./vendor-sortablejs-66a8dc70.js";const h={name:"DeviceMqttBat",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(a,d=void 0){this.$emit("update:configuration",{value:a,object:d})}}},b={class:"device-mqtt-bat"},f={class:"small"},g=e("br",null,null,-1),k=e("br",null,null,-1),v=e("span",{class:"text-info"},"-123",-1),x=e("br",null,null,-1),B=e("br",null,null,-1),I=e("span",{class:"text-info"},"123.45",-1),w=e("br",null,null,-1),W=e("br",null,null,-1),z=e("span",{class:"text-info"},"123.45",-1),N=e("br",null,null,-1),T=e("br",null,null,-1),q=e("span",{class:"text-info"},"95",-1);function D(a,d,i,E,y,F){const p=c("openwb-base-heading"),s=c("openwb-base-copy-to-clipboard"),r=c("openwb-base-alert");return _(),m("div",b,[n(p,null,{default:o(()=>[t(" Einstellungen für MQTT Batteriespeicher "),e("span",f,"(Modul: "+l(a.$options.name)+")",1)]),_:1}),n(r,{subtype:"info"},{default:o(()=>[e("ul",null,[e("li",null,[n(s,{class:"text-info",tooltip:"Topic kopieren"},{default:o(()=>[t("openWB/set/bat/"+l(i.componentId)+"/get/power",1)]),_:1}),g,t(" Speicherleistung in Watt, Zahl mit oder ohne Nachkommastellen (Float, Integer) und einem Punkt als Dezimaltrennzeichen, positiv Ladung, negativ Entladung"),k,t(" Beispiel: "),v]),e("li",null,[n(s,{class:"text-info",tooltip:"Topic kopieren"},{default:o(()=>[t("openWB/set/bat/"+l(i.componentId)+"/get/imported",1)]),_:1}),x,t(" Geladene Energie in Wh, Zahl mit oder ohne Nachkommastellen (Float, Integer) und einem Punkt als Dezimaltrennzeichen, nur positiv"),B,t(" Beispiel: "),I]),e("li",null,[n(s,{class:"text-info",tooltip:"Topic kopieren"},{default:o(()=>[t("openWB/set/bat/"+l(i.componentId)+"/get/exported",1)]),_:1}),w,t(" Entladene Energie in Wh, Zahl mit oder ohne Nachkommastellen (Float, Integer) und einem Punkt als Dezimaltrennzeichen, nur positiv"),W,t(" Beispiel: "),z]),e("li",null,[n(s,{class:"text-info",tooltip:"Topic kopieren"},{default:o(()=>[t("openWB/set/bat/"+l(i.componentId)+"/get/soc",1)]),_:1}),N,t(" Ladestand des Speichers, Zahl mit oder ohne Nachkommastellen (Float, Integer) und einem Punkt als Dezimaltrennzeichen, gültige Werte 0 bis 100"),T,t(" Beispiel: "),q])])]),_:1})])}const C=u(h,[["render",D],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/mqtt/bat.vue"]]);export{C as default};