import{D as d}from"./HardwareInstallation-a0083e3a.js";import{_ as u,u as t,k as l,l as p,D as i,N as m,y as c}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const v={name:"DeviceCarloGavazzi",mixins:[d]},_={class:"device-carlogavazzi"};function f(e,o,b,g,z,w){const r=t("openwb-base-heading"),s=t("openwb-base-text-input"),a=t("openwb-base-number-input");return l(),p("div",_,[i(r,null,{default:m(()=>[c(" Einstellungen für Carlo Gavazzi ")]),_:1}),i(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":e.device.configuration.ip_address,"onUpdate:modelValue":o[0]||(o[0]=n=>e.updateConfiguration(n,"configuration.ip_address"))},null,8,["model-value"]),i(a,{title:"Port",required:"",min:1,max:65535,"model-value":e.device.configuration.port,"onUpdate:modelValue":o[1]||(o[1]=n=>e.updateConfiguration(n,"configuration.port"))},null,8,["model-value"]),i(a,{title:"Modbus ID",required:"","model-value":e.device.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":o[2]||(o[2]=n=>e.updateConfiguration(n,"configuration.modbus_id"))},null,8,["model-value"])])}const U=u(v,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/carlo_gavazzi/carlo_gavazzi/device.vue"]]);export{U as default};