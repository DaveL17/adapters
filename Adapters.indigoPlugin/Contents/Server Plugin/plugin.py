#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""

import indigo  # noqa
import indigo_logging_handler
from sensor_adapter import SensorAdapter
# import logging
# import re
from pyrescaler.pyrescaler import *

DEBUGGING_ENABLED_MAP = {
    "y": True,
    "n": False
}


def _is_number(s):
    """
    Docstring placeholder
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


class Plugin(indigo.PluginBase):
    """
    Docstring placeholder
    """

    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        """
        Docstring placeholder
        """
        indigo.PluginBase.__init__(
            self, plugin_id, plugin_display_name, plugin_version, plugin_prefs
        )

        self.active_adapters = []
        self.adapters_for_device = {}
        self.debug = DEBUGGING_ENABLED_MAP[self.plugin_prefs['debuggingEnabled']]
        log_handler = indigo_logging_handler.IndigoLoggingHandler(self)

        self.log = logging.getLogger('indigo.temp-converter.plugin')
        self.log.addHandler(log_handler)
        logging.getLogger('pyrescaler').addHandler(log_handler)

        # "Subscribe to Changes" from all indigo devices, so we can update our 'converted'
        # temperature any time the native Temperature changes. Would be nice to only "Subscribe to
        # Changes" from individual objects, but that's not implemented yet.
        indigo.devices.subscribeToChanges()

    def __del__(self):
        """
        Docstring placeholder
        """
        indigo.PluginBase.__del__(self)

    def get_eligible_sensors(self, _filter="", values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        return [(f"{d.id:d}.{sk}", f"{d.name} ({sk}): {f'{float(sv):.1f}'}")
                for d in indigo.devices
                # don't include instances of this plugin/device in the list
                if (not d.pluginId) or (d.pluginId != self.pluginId)
                for (sk, sv) in d.states.items()
                # only return devices/states that have a numeric value
                if _is_number(sv)
                ]

    def validate_prefs_config_ui(self, values_dict):
        """
        Docstring placeholder
        """
        self.log.debug("validatePrefsConfigGui")
        self.update_logging(
            bool(values_dict['debuggingEnabled'] and "y" == values_dict['debuggingEnabled'])
        )
        return True

    def update_logging(self, is_debug):
        """
        Docstring placeholder
        """
        if is_debug:
            self.debug = True
            self.log.setLevel(logging.DEBUG)
            logging.getLogger("indigo.temp-converter.plugin").setLevel(logging.DEBUG)
            logging.getLogger("pyrescaler").setLevel(logging.DEBUG)
            self.log.debug("debug logging enabled")
        else:
            self.log.debug("debug logging disabled")
            self.debug = False
            self.log.setLevel(logging.INFO)
            logging.getLogger("indigo.temp-converter.plugin").setLevel(logging.INFO)
            logging.getLogger("pyrescaler").setLevel(logging.INFO)

    def startup(self):
        """
        Docstring placeholder
        """
        self.log.debug("startup called")
        if "debuggingEnabled" not in self.pluginPrefs:
            self.pluginPrefs["debuggingEnabled"] = "n"

        self.update_logging(DEBUGGING_ENABLED_MAP[self.pluginPrefs["debuggingEnabled"]])

    def shutdown(self):
        """
        Docstring placeholder
        """
        self.log.debug("shutdown called")

    def open_browser_to_python_format_help(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.browserOpen("https://pyformat.info")

    def address_changed(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.log.debug("address_changed")

    def scale_type_changed(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.log.debug("scale_type_changed")

    def get_scales(self, _filter="", values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.log.debug("get_scales")
        if "scaleType" not in values_dict:
            return []
        self.log.debug(f"getting scale options for scale type: {values_dict['scaleType']}")
        opts = get_scale_options(scale_type=values_dict["scaleType"])
        self.log.debug(f"scale options: {opts}")
        return opts

    def device_start_comm(self, dev):
        """
        Docstring placeholder
        """
        self.log.debug(f"device_start_comm: {dev.pluginProps['address']}")
        # in case any states added/removed after plugin upgrade
        dev.stateListOrDisplayStateIdChanged()

        new_device = SensorAdapter(dev)
        self.active_adapters.append(new_device)

        if new_device.native_device_id not in self.adapters_for_device:
            self.adapters_for_device[new_device.native_device_id] = []

        self.adapters_for_device[new_device.native_device_id].append(new_device)

        self.log.debug(f"added adapter: {new_device.name()}")

    def device_stop_comm(self, dev):
        """
        Docstring placeholder
        """
        self.active_adapters = [
            rs for rs in self.active_adapters
            if rs.address != dev.pluginProps["address"]
        ]

    def device_updated(self, orig_dev, new_dev):
        """
        Docstring placeholder
        """
        indigo.PluginBase.device_updated(self, orig_dev, new_dev)
        if new_dev.id in self.adapters_for_device:
            for cs in self.adapters_for_device[new_dev.id]:
                cs.go()

    def run_concurrent_thread(self):
        """
        Docstring placeholder
        """
        try:

            while True:
                self.sleep(5)

        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.
