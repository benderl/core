import{D as a}from"./HardwareInstallation-774805b0.js";import{_ as p,u as s,l as m,m as u,G as n,E as d,y as l}from"./vendor-0c15df0c.js";import"./vendor-fortawesome-231ff303.js";import"./index-6ffbdc7e.js";import"./vendor-bootstrap-83e2d5a1.js";import"./vendor-jquery-84e2bf4a.js";import"./vendor-axios-c9d2afa0.js";import"./vendor-sortablejs-1a751103.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceSmartMe",mixins:[a]},f={class:"device-smart-me"};function v(o,e,_,b,g,w){const r=s("openwb-base-heading"),i=s("openwb-base-text-input");return m(),u("div",f,[n(r,null,{default:d(()=>e[2]||(e[2]=[l(" Einstellungen für smart-me ")])),_:1}),n(i,{title:"Benutzername",subtype:"user",required:"","model-value":o.device.configuration.user,"onUpdate:modelValue":e[0]||(e[0]=t=>o.updateConfiguration(t,"configuration.user"))},null,8,["model-value"]),n(i,{title:"Passwort",subtype:"password",required:"","model-value":o.device.configuration.password,"onUpdate:modelValue":e[1]||(e[1]=t=>o.updateConfiguration(t,"configuration.password"))},null,8,["model-value"])])}const q=p(c,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/smart_me/smart_me/device.vue"]]);export{q as default};