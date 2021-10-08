""" Modul, um die Daten vom Broker zu erhalten.
"""
import importlib
import json
import paho.mqtt.client as mqtt
import re

from ..algorithm import bat
from ..algorithm import chargelog
from ..algorithm import chargepoint
from ..algorithm import counter
from ..algorithm import ev
from ..algorithm import general
from . import log
from ..algorithm import optional
from . import pub
from . import system
from ..algorithm import pv


class subData():
    """ Klasse, die die benötigten Topics abonniert, die Instanzen ertstellt, wenn z.b. ein Modul neu konfiguriert wird, 
    Instanzen löscht, wenn Module gelöscht werden, und die Werte in die Attribute der Instanzen schreibt.
    """

    # Instanzen
    cp_data = {}
    cp_template_data = {}
    pv_data = {}
    pv_module_data = {}
    ev_data = {}
    ev_template_data = {}
    ev_charge_template_data = {}
    counter_data = {}
    counter_module_data = {}
    bat_data = {}
    bat_module_data = {}
    general_data = {}
    optional_data = {}
    system_data = {}
    defaults_cp_data = {}
    defaults_cp_template_data = {}
    defaults_pv_data = {}
    defaults_ev_data = {}
    defaults_ev_template_data = {}
    defaults_ev_charge_template_data = {}
    defaults_counter_data = {}
    defaults_bat_data = {}
    defaults_general_data = {}
    defaults_optional_data = {}
    defaults_system_data = {}

    def __init__(self, event_ev_template, event_charge_template, event_cp_config):
        self.event_ev_template = event_ev_template
        self.event_charge_template = event_charge_template
        self.event_cp_config = event_cp_config
        self.heartbeat = False

    def sub_topics(self):
        """ abonniert alle Topics.
        """
        try:
            mqtt_broker_ip = "localhost"
            client = mqtt.Client("openWB-mqttsub-" + self.getserial())
            # ipallowed='^[0-9.]+$'
            # nameallowed='^[a-zA-Z ]+$'
            # namenumballowed='^[0-9a-zA-Z ]+$'

            client.on_connect = self.on_connect
            client.on_message = self.on_message

            client.connect(mqtt_broker_ip, 1886)
            client.loop_forever()
            client.disconnect()
        except Exception as e:
            log.exception_logging(e)

    def getserial(self):
        """ Extract serial from cpuinfo file
        """
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line[0:6] == 'Serial':
                    return line[10:26]
            return "0000000000000000"

    def on_connect(self, client, userdata, flags, rc):
        """ connect to broker and subscribe to set topics
        """
        client.subscribe("openWB/vehicle/#", 2)
        client.subscribe("openWB/chargepoint/#", 2)
        client.subscribe("openWB/pv/#", 2)
        client.subscribe("openWB/bat/#", 2)
        client.subscribe("openWB/general/#", 2)
        client.subscribe("openWB/optional/#", 2)
        client.subscribe("openWB/counter/#", 2)
        client.subscribe("openWB/defaults/#", 2)
        client.subscribe("openWB/log/#", 2)
        client.subscribe("openWB/system/#", 2)

    def on_message(self, client, userdata, msg):
        """ wartet auf eingehende Topics.
        """
        log.message_mqtt_log(str(msg.topic), str(msg.payload.decode("utf-8")))
        self.heartbeat = True
        if "openWB/vehicle/template/charge_template/" in msg.topic:
            self.process_vehicle_charge_template_topic(self.ev_charge_template_data, msg)
        elif "openWB/defaults/vehicle/template/charge_template/" in msg.topic:
            self.process_vehicle_charge_template_topic(self.defaults_ev_charge_template_data, msg)
        elif "openWB/vehicle/template/ev_template/" in msg.topic:
            self.process_vehicle_ev_template_topic(self.ev_template_data, msg)
        elif "openWB/defaults/vehicle/template/ev_template/" in msg.topic:
            self.process_vehicle_ev_template_topic(self.defaults_ev_template_data, msg)
        elif "openWB/vehicle/" in msg.topic:
            self.process_vehicle_topic(self.ev_data, msg)
        elif "openWB/defaults/vehicle/" in msg.topic:
            self.process_vehicle_topic(self.defaults_ev_data, msg, True)
        elif "openWB/chargepoint/template/" in msg.topic:
            self.process_chargepoint_template_topic(self.cp_template_data, msg)
        elif "openWB/defaults/chargepoint/template/" in msg.topic:
            self.process_chargepoint_template_topic(self.defaults_cp_template_data, msg)
        elif "openWB/chargepoint/" in msg.topic:
            self.process_chargepoint_topic(self.cp_data, msg)
        elif "openWB/defaults/chargepoint/" in msg.topic:
            self.process_chargepoint_topic(self.defaults_cp_data, msg, True)
        elif "openWB/pv/" in msg.topic and "/module/" in msg.topic:
            self.process_pv_module_topic(self.pv_data, msg)
        elif "openWB/pv/" in msg.topic:
            self.process_pv_topic(self.pv_data, msg)
        elif "openWB/defaults/pv/" in msg.topic:
            self.process_pv_topic(self.defaults_pv_data, msg)
        elif "openWB/bat/" in msg.topic and "/module/" in msg.topic:
            self.process_bat_module_topic(self.bat_data, msg)
        elif "openWB/bat/" in msg.topic:
            self.process_bat_topic(self.bat_data, msg)
        elif "openWB/defaults/bat/" in msg.topic:
            self.process_bat_topic(self.defaults_bat_data, msg)
        elif "openWB/general/" in msg.topic:
            self.process_general_topic(self.general_data, msg)
        elif "openWB/defaults/general/" in msg.topic:
            self.process_general_topic(self.defaults_general_data, msg)
        elif "openWB/optional/" in msg.topic:
            self.process_optional_topic(self.optional_data, msg)
        elif "openWB/defaults/optional/" in msg.topic:
            self.process_optional_topic(self.defaults_optional_data, msg, True)
        elif re.search("^openWB/counter/[0-9]+/module.*$", msg.topic) != None:
            self.process_counter_module_topic(self.counter_module_data, msg)
        elif "openWB/counter/" in msg.topic:
            self.process_counter_topic(self.counter_data, msg)
        elif "openWB/defaults/counter/" in msg.topic:
            self.process_counter_topic(self.defaults_counter_data, msg, True)
        elif "openWB/log/" in msg.topic:
            self.process_log_topic(msg)
        elif "openWB/system/" in msg.topic:
            self.process_system_topic(self.system_data, msg)
        elif "openWB/defaults/system" in msg.topic:
            self.process_system_topic(self.defaults_system_data, msg)
        else:
            log.message_debug_log("warning", "unknown subdata-topic: "+str(msg.topic))

    def get_index(self, topic):
        """extrahiert den Index aus einem Topic (Zahl zwischen zwei // oder am Stringende)

         Parameters
        ----------
        topic : str
            Topic, aus dem der Index extrahiert wird
        """
        index = re.search('(?!/)([0-9]*)(?=/|$)', topic)
        return index.group()

    def get_second_index(self, topic):
        """extrahiert den zweiten Index aus einem Topic (Zahl zwischen zwei //)

            Parameters
        ----------
        topic : str
            Topic, aus dem der Index extrahiert wird
        """
        index = re.search('^.+/([0-9]*)/.+/([0-9]+)/.+$', topic)
        return index.group(2)

    def set_json_payload(self, dict, msg):
        """ dekodiert das JSON-Objekt und setzt diesen für den Value in das übergebene Dictionary, als Key wird der Name nach dem letzten / verwendet.

         Parameters
        ----------
        dict : dictionary
            Dictionary, in dem der Wert abgelegt wird
        msg : 
            enthält den Payload als json-Objekt
        """
        try:
            key = re.search("/([a-z,A-Z,0-9,_]+)(?!.*/)", msg.topic).group(1)
            if msg.payload:
                dict[key] = json.loads(str(msg.payload.decode("utf-8")))
            else:
                if key in dict:
                    dict.pop(key)
        except Exception as e:
            log.exception_logging(e)

    def process_vehicle_topic(self, var, msg, default=False):
        """ Handler für die EV-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/vehicle/[0-9]+/.+$", msg.topic) != None:
                if "ev"+index not in var:
                    var["ev"+index] = ev.ev(int(index), default)
                if re.search("^.+/vehicle/[0-9]+$", msg.topic) != None:
                    if json.loads(str(msg.payload.decode("utf-8"))) == "":
                        if "ev"+index in var:
                            var.pop("ev"+index)
                else:
                    if re.search("^.+/vehicle/[0-9]+/get.+$", msg.topic) != None:
                        if "get" not in var["ev"+index].data:
                            var["ev"+index].data["get"] = {}
                        self.set_json_payload(var["ev"+index].data["get"], msg)
                    elif re.search("^.+/vehicle/[0-9]+/set.+$", msg.topic) != None:
                        if "set" not in var["ev"+index].data:
                            var["ev"+index].data["set"] = {}
                        self.set_json_payload(var["ev"+index].data["set"], msg)
                    elif re.search("^.+/vehicle/[0-9]+/soc/config/.+$", msg.topic) != None:
                        if "soc" not in var["ev"+index].data:
                            var["ev"+index].data["soc"] = {}
                        if "config" not in var["ev"+index].data["soc"]:
                            var["ev"+index].data["soc"]["config"] = {}
                        self.set_json_payload(var["ev"+index].data["soc"]["config"], msg)
                    elif re.search("^.+/vehicle/[0-9]+/soc/get/.+$", msg.topic) != None:
                        if "soc" not in var["ev"+index].data:
                            var["ev"+index].data["soc"] = {}
                        if "get" not in var["ev"+index].data["soc"]:
                            var["ev"+index].data["soc"]["get"] = {}
                        self.set_json_payload(var["ev"+index].data["soc"]["get"], msg)
                    elif re.search("^.+/vehicle/[0-9]+/control_parameter/.+$", msg.topic) != None:
                        if "control_parameter" not in var["ev"+index].data:
                            var["ev"+index].data["control_parameter"] = {}
                        self.set_json_payload(var["ev"+index].data["control_parameter"], msg)
                    else:
                        self.set_json_payload(var["ev"+index].data, msg)
        except Exception as e:
            log.exception_logging(e)

    def process_vehicle_charge_template_topic(self, var, msg):
        """ Handler für die EV-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/vehicle/template/charge_template/[0-9]+$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "ct"+index in var:
                        var.pop("ct"+index)
                else:
                    if "ct"+index not in var:
                        var["ct"+index] = ev.chargeTemplate(int(index))
                    var["ct"+index].data = json.loads(str(msg.payload.decode("utf-8")))
                    self.event_charge_template.set()
        except Exception as e:
            log.exception_logging(e)

    def process_vehicle_ev_template_topic(self, var, msg):
        """ Handler für die EV-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/vehicle/template/ev_template/[0-9]+$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "et"+index in var:
                        var.pop("et"+index)
                else:
                    if "et"+index not in var:
                        var["et"+index] = ev.evTemplate(int(index))
                    var["et"+index].data = json.loads(str(msg.payload.decode("utf-8")))
                    self.event_ev_template.set()
        except Exception as e:
            log.exception_logging(e)

    def process_chargepoint_topic(self, var, msg, default=False):
        """ Handler für die Ladepunkt-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/chargepoint/[0-9]+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "cp"+index in var:
                        var.pop("cp"+index)
            elif re.search("^.+/chargepoint/[0-9]+/.+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if "cp"+index not in var:
                    var["cp"+index] = chargepoint.chargepoint(int(index), default)
                if "all" not in var:
                    var["all"] = chargepoint.allChargepoints()
                if re.search("^.+/chargepoint/[0-9]+/set/.+$", msg.topic) != None:
                    if "set" not in var["cp"+index].data:
                        var["cp"+index].data["set"] = {}
                    if re.search("^.+/chargepoint/[0-9]+/set/log/.+$", msg.topic) != None:
                        if "log" not in var["cp"+index].data["set"]:
                            var["cp"+index].data["set"]["log"] = {}
                        self.set_json_payload(var["cp"+index].data["set"]["log"], msg)
                    else:
                        self.set_json_payload(var["cp"+index].data["set"], msg)
                elif re.search("^.+/chargepoint/[0-9]+/get/.+$", msg.topic) != None:
                    if "get" not in var["cp"+index].data:
                        var["cp"+index].data["get"] = {}
                    if re.search("^.+/chargepoint/[0-9]+/get/connected_vehicle/.+$", msg.topic) != None:
                        if "connected_vehicle" not in var["cp"+index].data["get"]:
                            var["cp"+index].data["get"]["connected_vehicle"] = {}
                        self.set_json_payload(var["cp"+index].data["get"]["connected_vehicle"], msg)
                    elif re.search("^.+/chargepoint/[0-9]+/get/.+$", msg.topic) != None:
                        self.set_json_payload(var["cp"+index].data["get"], msg)
                elif re.search("^.+/chargepoint/[0-9]+/config$", msg.topic) != None:
                    self.set_json_payload(var["cp"+index].data, msg)
                    self.event_cp_config.set()
            elif re.search("^.+/chargepoint/get/.+$", msg.topic) != None:
                if "all" not in var:
                    var["all"] = chargepoint.allChargepoints()
                self.set_json_payload(var["all"].data["get"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_chargepoint_template_topic(self, var, msg):
        """ Handler für die Ladepunkt-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/chargepoint/template/[0-9]+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if json.loads(str(msg.payload.decode("utf-8"))) == 1:
                    if "cpt"+index not in var:
                        var["cpt"+index] = chargepoint.cpTemplate()
                else:
                    if "cpt"+index in var:
                        var.pop("cpt"+index)
            elif re.search("^.+/chargepoint/template/[0-9]+/.+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if "cpt"+index not in var:
                    var["cpt"+index] = chargepoint.cpTemplate()
                if re.search("^.+/chargepoint/template/[0-9]+/autolock/.+$", msg.topic) != None:
                    if "autolock" not in var["cpt"+index].data:
                        var["cpt"+index].data["autolock"] = {}
                    if re.search("^.+/chargepoint/template/[0-9]+/autolock/[0-9]+/.+$", msg.topic) != None:
                        index_second = self.get_second_index(msg.topic)
                        if "plan"+index_second not in var["cpt"+index].data["autolock"]:
                            var["cpt"+index].data["autolock"]["plan"+index_second] = {}
                        if re.search("^.+/chargepoint/template/[0-9]+/autolock/[0-9]+/frequency/.+$", msg.topic) != None:
                            if "frequency" not in var["cpt"+index].data["autolock"]["plan"+index_second]:
                                var["cpt"+index].data["autolock"]["plan"+index_second]["frequency"] = {}
                            self.set_json_payload(var["cpt"+index].data["autolock"]["plan"+index_second]["frequency"], msg)
                        else:
                            self.set_json_payload(var["cpt"+index].data["autolock"]["plan"+index_second], msg)
                    else:
                        self.set_json_payload(var["cpt"+index].data["autolock"], msg)
                else:
                    self.set_json_payload(var["cpt"+index].data, msg)
        except Exception as e:
            log.exception_logging(e)

    def process_pv_topic(self, var, msg):
        """ Handler für die PV-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/pv$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "all" in var:
                        var.pop("all")
            elif re.search("^.+/pv/[0-9]+/.+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if "all" not in var:
                    var["all"] = pv.pvAll()
                if "pv"+index not in var:
                    var["pv"+index] = pv.pv(int(index))
                if re.search("^.+/pv/[0-9]+/config$", msg.topic) != None:
                    self.set_json_payload(var["pv"+index].data, msg)
                elif re.search("^.+/pv/[0-9]+/get/.+$", msg.topic) != None:
                    if "get" not in var["pv"+index].data:
                        var["pv"+index].data["get"] = {}
                    self.set_json_payload(var["pv"+index].data["get"], msg)
            elif re.search("^.+/pv/.+$", msg.topic) != None:
                if "all" not in var:
                    var["all"] = pv.pvAll()
                if re.search("^.+/pv/config/.+$", msg.topic) != None:
                    if "config" not in var["all"].data:
                        var["all"].data["config"] = {}
                    self.set_json_payload(var["all"].data["config"], msg)
                elif re.search("^.+/pv/get/.+$", msg.topic) != None:
                    if "get" not in var["all"].data:
                        var["all"].data["get"] = {}
                    self.set_json_payload(var["all"].data["get"], msg)
                elif re.search("^.+/pv/set/.+$", msg.topic) != None:
                    if "set" not in var["all"].data:
                        var["all"].data["set"] = {}
                    self.set_json_payload(var["all"].data["set"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_pv_module_topic(self, var, msg):
        """ Handler für die Wechselrichter-Modul-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/pv/[0-9]+/module$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "pv"+index in var:
                        var.pop("pv"+index)
                else:
                    data = json.loads(str(msg.payload.decode("utf-8")))
                    mod = importlib.import_module(".modules.pv."+data["selected"], "packages")
                    var["pv"+index] = mod.module(index)
                    self.set_json_payload(var["pv"+index].data, msg)
            elif re.search("^.+/pv/[0-9]+/module/simulation/.+$", msg.topic) != None:
                if "simulation" not in var["pv"+index].data:
                    var["pv"+index].data["simulation"] = {}
                self.set_json_payload(var["pv"+index].data["simulation"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_bat_topic(self, var, msg):
        """ Handler für die Hausspeicher-Hardware_Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/bat$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "all" in var:
                        var.pop("all")
            elif re.search("^.+/bat/[0-9]+/.+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if "all" not in var:
                    var["all"] = bat.batAll()
                if "bat"+index not in var:
                    var["bat"+index] = bat.bat(int(index))
                if re.search("^.+/bat/[0-9]+/config$", msg.topic) != None:
                    self.set_json_payload(var["bat"+index].data, msg)
                elif re.search("^.+/bat/[0-9]+/get/.+$", msg.topic) != None:
                    if "get" not in var["bat"+index].data:
                        var["bat"+index].data["get"] = {}
                    self.set_json_payload(var["bat"+index].data["get"], msg)
                elif re.search("^.+/bat/[0-9]+/set/.+$", msg.topic) != None:
                    if "set" not in var["bat"+index].data:
                        var["bat"+index].data["set"] = {}
                    self.set_json_payload(var["bat"+index].data["set"], msg)
            elif re.search("^.+/bat/.+$", msg.topic) != None:
                if "all" not in var:
                    var["all"] = bat.batAll()
                if re.search("^.+/bat/get/.+$", msg.topic) != None:
                    if "get" not in var["all"].data:
                        var["all"].data["get"] = {}
                    self.set_json_payload(var["all"].data["get"], msg)
                elif re.search("^.+/bat/set/.+$", msg.topic) != None:
                    if "set" not in var["all"].data:
                        var["all"].data["set"] = {}
                    self.set_json_payload(var["all"].data["set"], msg)
                elif re.search("^.+/bat/config/.+$", msg.topic) != None:
                    if "config" not in var["all"].data:
                        var["all"].data["config"] = {}
                    self.set_json_payload(var["all"].data["config"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_bat_module_topic(self, var, msg):
        """ Handler für die Speicher-Modul-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/bat/[0-9]+/module$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "bat"+index in var:
                        var.pop("bat"+index)
                else:
                    data = json.loads(str(msg.payload.decode("utf-8")))
                    mod = importlib.import_module(".modules.bat."+data["selected"], "packages")
                    var["bat"+index] = mod.module(index)
                    self.set_json_payload(var["bat"+index].data, msg)
            elif re.search("^.+/bat/[0-9]+/module/simulation/.+$", msg.topic) != None:
                if "simulation" not in var["bat"+index].data:
                    var["bat"+index].data["simulation"] = {}
                self.set_json_payload(var["bat"+index].data["simulation"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_general_topic(self, var, msg):
        """ Handler für die Allgemeinen-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/general/.+$", msg.topic) != None:
                if "general" not in var:
                    var["general"] = general.general()
                if re.search("^.+/general/notifications/.+$", msg.topic) != None:
                    if "notifications" not in var["general"].data:
                        var["general"].data["notifications"] = {}
                    self.set_json_payload(var["general"].data["notifications"], msg)
                elif re.search("^.+/general/ripple_control_receiver/.+$", msg.topic) != None:
                    if "ripple_control_receiver" not in var["general"].data:
                        var["general"].data["ripple_control_receiver"] = {}
                    self.set_json_payload(var["general"].data["ripple_control_receiver"], msg)
                elif re.search("^.+/general/chargemode_config/.+$", msg.topic) != None:
                    if "chargemode_config" not in var["general"].data:
                        var["general"].data["chargemode_config"] = {}
                    if re.search("^.+/general/chargemode_config/pv_charging/.+$", msg.topic) != None:
                        if "pv_charging" not in var["general"].data["chargemode_config"]:
                            var["general"].data["chargemode_config"]["pv_charging"] = {}
                        self.set_json_payload(var["general"].data["chargemode_config"]["pv_charging"], msg)
                    elif re.search("^.+/general/chargemode_config/instant_charging/.+$", msg.topic) != None:
                        if "instant_charging" not in var["general"].data["chargemode_config"]:
                            var["general"].data["chargemode_config"]["instant_charging"] = {}
                        self.set_json_payload(var["general"].data["chargemode_config"]["instant_charging"], msg)
                    elif re.search("^.+/general/chargemode_config/scheduled_charging/.+$", msg.topic) != None:
                        if "scheduled_charging" not in var["general"].data["chargemode_config"]:
                            var["general"].data["chargemode_config"]["scheduled_charging"] = {}
                        self.set_json_payload(var["general"].data["chargemode_config"]["scheduled_charging"], msg)
                    elif re.search("^.+/general/chargemode_config/time_charging/.+$", msg.topic) != None:
                        if "time_charging" not in var["general"].data["chargemode_config"]:
                            var["general"].data["chargemode_config"]["time_charging"] = {}
                        self.set_json_payload(var["general"].data["chargemode_config"]["time_charging"], msg)
                    elif re.search("^.+/general/chargemode_config/standby/.+$", msg.topic) != None:
                        if "standby" not in var["general"].data["chargemode_config"]:
                            var["general"].data["chargemode_config"]["standby"] = {}
                        self.set_json_payload(var["general"].data["chargemode_config"]["standby"], msg)
                    else:
                        self.set_json_payload(var["general"].data["chargemode_config"], msg)
                else:
                    self.set_json_payload(var["general"].data, msg)
        except Exception as e:
            log.exception_logging(e)

    def process_optional_topic(self, var, msg, default=False):
        """ Handler für die Optionalen-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/optional/.+$", msg.topic) != None:
                if "optional" not in var:
                    var["optional"] = optional.optional(default)
                if re.search("^.+/optional/led/.+$", msg.topic) != None:
                    if "led" not in var["optional"].data:
                        var["optional"].data["led"] = {}
                    self.set_json_payload(var["optional"].data["led"], msg)
                elif re.search("^.+/optional/rfid/.+$", msg.topic) != None:
                    if "rfid" not in var["optional"].data:
                        var["optional"].data["rfid"] = {}
                    self.set_json_payload(var["optional"].data["rfid"], msg)
                elif re.search("^.+/optional/int_display/.+$", msg.topic) != None:
                    if "int_display" not in var["optional"].data:
                        var["optional"].data["int_display"] = {}
                    self.set_json_payload(var["optional"].data["int_display"], msg)
                elif re.search("^.+/optional/et/.+$", msg.topic) != None:
                    if "et" not in var["optional"].data:
                        var["optional"].data["et"] = {}
                    if re.search("^.+/optional/et/get/.+$", msg.topic) != None:
                        if "get" not in var["optional"].data["et"]:
                            var["optional"].data["et"]["get"] = {}
                        self.set_json_payload(var["optional"].data["et"]["get"], msg)
                    elif re.search("^.+/optional/et/config/.+$", msg.topic) != None:
                        if "config" not in var["optional"].data["et"]:
                            var["optional"].data["et"]["config"] = {}
                        self.set_json_payload(var["optional"].data["et"]["config"], msg)
                    else:
                        self.set_json_payload(var["optional"].data["et"], msg)
                else:
                    self.set_json_payload(var["optional"].data, msg)
        except Exception as e:
            log.exception_logging(e)

    def process_counter_topic(self, var, msg, default=False):
        """ Handler für die Zähler-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if re.search("^.+/counter/[0-9]+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "counter"+index in var:
                        var.pop("counter"+index)
            elif re.search("^.+/counter/[0-9]+/.+$", msg.topic) != None:
                index = self.get_index(msg.topic)
                if "counter"+index not in var:
                    var["counter"+index] = counter.counter(int(index), default)
                if re.search("^.+/counter/[0-9]+/get.+$", msg.topic) != None:
                    if "get" not in var["counter"+index].data:
                        var["counter"+index].data["get"] = {}
                    self.set_json_payload(var["counter"+index].data["get"], msg)
                elif re.search("^.+/counter/[0-9]+/set.+$", msg.topic) != None:
                    if "set" not in var["counter"+index].data:
                        var["counter"+index].data["set"] = {}
                    self.set_json_payload(var["counter"+index].data["set"], msg)
                elif re.search("^.+/counter/[0-9]+/config/.+$", msg.topic) != None:
                    if "config" not in var["counter"+index].data:
                        var["counter"+index].data["config"] = {}
                    self.set_json_payload(var["counter"+index].data["config"], msg)
            elif re.search("^.+/counter/.+$", msg.topic) != None:
                if "all" not in var:
                    var["all"] = counter.counterAll()
                if re.search("^.+/counter/get.+$", msg.topic) != None:
                    if "get" not in var["all"].data:
                        var["all"].data["get"] = {}
                    self.set_json_payload(var["all"].data["get"], msg)
                elif re.search("^.+/counter/set.+$", msg.topic) != None:
                    if "set" not in var["all"].data:
                        var["all"].data["set"] = {}
                    self.set_json_payload(var["all"].data["set"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_counter_module_topic(self, var, msg):
        """ Handler für die Zähler-MOdul-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            index = self.get_index(msg.topic)
            if re.search("^.+/counter/[0-9]+/module$", msg.topic) != None:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "counter"+index in var:
                        var.pop("counter"+index)
                else:
                    data = json.loads(str(msg.payload.decode("utf-8")))
                    mod = importlib.import_module(".modules.counter."+data["selected"], "packages")
                    var["counter"+index] = mod.module(index)
                    self.set_json_payload(var["counter"+index].data, msg)
            elif re.search("^.+/counter/[0-9]+/module/simulation/.+$", msg.topic) != None:
                if "simulation" not in var["counter"+index].data:
                    var["counter"+index].data["simulation"] = {}
                self.set_json_payload(var["counter"+index].data["simulation"], msg)
        except Exception as e:
            log.exception_logging(e)

    def process_log_topic(self, msg):
        """Handler für die Log-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if "openWB/log/request" in msg.topic:
                chargelog.get_log_data(json.loads(str(msg.payload.decode("utf-8"))))
        except Exception as e:
            log.exception_logging(e)

    def process_system_topic(self, var, msg):
        """Handler für die System-Topics

         Parameters
        ----------
        client : (unused)
            vorgegebener Parameter
        userdata : (unused)
            vorgegebener Parameter
        msg:
            enthält Topic und Payload
        """
        try:
            if "system" not in var:
                if json.loads(str(msg.payload.decode("utf-8"))) == "":
                    if "system" in var:
                        var.pop("system")
                else:
                    var["system"] = system.system()
            self.set_json_payload(var["system"].data, msg)
        except Exception as e:
            log.exception_logging(e)