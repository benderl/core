import{D as p}from"./HardwareInstallation-775406e1.js";import{_ as m,u as t,k as b,l as f,G as i,E as s,y as r,x as v}from"./vendor-06e11d0e.js";import"./vendor-fortawesome-3d19d475.js";import"./index-beac009d.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const w={name:"DeviceHuawei",mixins:[p]},c={class:"device-huawei"};function g(n,e,_,h,D,V){const l=t("openwb-base-heading"),u=t("openwb-base-alert"),d=t("openwb-base-text-input"),a=t("openwb-base-number-input");return b(),f("div",c,[i(l,null,{default:s(()=>e[3]||(e[3]=[r(" Einstellungen für Huawei ")])),_:1}),i(u,{subtype:"info"},{default:s(()=>e[4]||(e[4]=[r(' Die Antwort der Huawei Wechselrichter benötigt sehr viel Zeit. Es wird empfohlen, dass Regelintervall der openWB auf "sehr langsam" zu stellen. ')])),_:1}),i(d,{title:"IP oder Hostname",subtype:"host",required:"","model-value":n.device.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=o=>n.updateConfiguration(o,"configuration.ip_address"))},null,8,["model-value"]),i(a,{title:"Port",required:"",min:1,max:65535,"model-value":n.device.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=o=>n.updateConfiguration(o,"configuration.port"))},null,8,["model-value"]),i(a,{title:"Modbus ID",required:"","model-value":n.device.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":e[2]||(e[2]=o=>n.updateConfiguration(o,"configuration.modbus_id"))},{help:s(()=>e[5]||(e[5]=[r(' Sind mehrere Huawei Wechselrichter als "Schwarm" verbunden, dann besitzt der Master vermutlich die ID "16". Über diese ID werden dann alle Daten in Summe zur Verfügung gestellt.'),v("br",null,null,-1),r(" Die IDs 1 bis 15 sind für einzelne Wechselrichter reserviert. ")])),_:1},8,["model-value"])])}const k=m(w,[["render",g],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/huawei/huawei/device.vue"]]);export{k as default};