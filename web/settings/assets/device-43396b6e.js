import{D as p}from"./HardwareInstallation-b6711c62.js";import{_ as u,u as n,k as d,l as m,G as i,E as l,y as _}from"./vendor-f90150d8.js";import"./vendor-fortawesome-8488187c.js";import"./index-84ae27ac.js";import"./vendor-bootstrap-99f0c261.js";import"./vendor-jquery-99ccf6d7.js";import"./vendor-axios-871a0510.js";import"./vendor-sortablejs-cfc19546.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceHuaweiSmartLogger",mixins:[p]},g={class:"device-huawei-smart-logger"};function f(o,e,b,v,w,x){const r=n("openwb-base-heading"),a=n("openwb-base-text-input"),s=n("openwb-base-number-input");return d(),m("div",g,[i(r,null,{default:l(()=>e[2]||(e[2]=[_(" Einstellungen für Huawei SmartLogger ")])),_:1}),i(a,{title:"IP oder Hostname",subtype:"host",required:"","model-value":o.device.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=t=>o.updateConfiguration(t,"configuration.ip_address"))},null,8,["model-value"]),i(s,{title:"Port",required:"",min:1,max:65535,"model-value":o.device.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=t=>o.updateConfiguration(t,"configuration.port"))},null,8,["model-value"])])}const q=u(c,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/huawei/huawei_smartlogger/device.vue"]]);export{q as default};