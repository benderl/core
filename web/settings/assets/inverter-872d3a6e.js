import{C as m}from"./HardwareInstallation-2b28bae8.js";import{_ as d,u as o,k as u,l,G as t,E as i,y as r}from"./vendor-809787c9.js";import"./vendor-fortawesome-e760f6db.js";import"./index-b3b3d3af.js";import"./vendor-bootstrap-5ce91dd7.js";import"./vendor-jquery-49acc558.js";import"./vendor-axios-57a82265.js";import"./vendor-sortablejs-d99a4022.js";import"./dynamic-import-helper-be004503.js";const g={name:"DeviceSigenergyInverter",mixins:[m]},_={class:"device-sigenergy-inverter"};function c(n,e,b,f,v,y){const s=o("openwb-base-heading"),p=o("openwb-base-number-input");return u(),l("div",_,[t(s,null,{default:i(()=>e[1]||(e[1]=[r(" Einstellungen für Sigenergy Wechselrichter ")])),_:1}),t(p,{title:"Modbus ID",required:"","model-value":n.component.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":e[0]||(e[0]=a=>n.updateConfiguration(a,"configuration.modbus_id"))},{help:i(()=>e[2]||(e[2]=[r(" Die Standard-Modbus-ID von Sigenergy ist 247 ")])),_:1},8,["model-value"])])}const I=d(g,[["render",c],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/sigenergy/sigenergy/inverter.vue"]]);export{I as default};