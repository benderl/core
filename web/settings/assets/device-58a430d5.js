import{D as r}from"./HardwareInstallation-a0083e3a.js";import{_ as d,u as t,k as l,l as u,D as i,N as m,y as c}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const _={name:"DeviceOpenwbFlex",mixins:[r]},b={class:"device-openwb-flex"};function f(e,o,v,w,g,x){const p=t("openwb-base-heading"),s=t("openwb-base-text-input"),a=t("openwb-base-number-input");return l(),u("div",b,[i(p,null,{default:m(()=>[c(" Einstellungen für openWB-Flex ")]),_:1}),i(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":e.device.configuration.ip_address,"onUpdate:modelValue":o[0]||(o[0]=n=>e.updateConfiguration(n,"configuration.ip_address"))},null,8,["model-value"]),i(a,{title:"Port",required:"",min:1,max:65535,"model-value":e.device.configuration.port,"onUpdate:modelValue":o[1]||(o[1]=n=>e.updateConfiguration(n,"configuration.port"))},null,8,["model-value"])])}const y=d(_,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/openwb/openwb_flex/device.vue"]]);export{y as default};