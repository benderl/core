import{D as a}from"./HardwareInstallation-a0083e3a.js";import{_ as p,u as t,k as c,l as d,D as n,N as m,y as l}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const u={name:"DeviceRCT",mixins:[a]},_={class:"device-rct"};function f(e,o,v,b,g,x){const i=t("openwb-base-heading"),s=t("openwb-base-text-input");return c(),d("div",_,[n(i,null,{default:m(()=>[l(" Einstellungen für RCT ")]),_:1}),n(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":e.device.configuration.ip_address,"onUpdate:modelValue":o[0]||(o[0]=r=>e.updateConfiguration(r,"configuration.ip_address"))},null,8,["model-value"])])}const V=p(u,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/rct/rct/device.vue"]]);export{V as default};