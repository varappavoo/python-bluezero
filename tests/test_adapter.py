import sys
import subprocess
import unittest
import dbus
import dbus.mainloop.glib
import dbusmock
from gi.repository import GLib
from bluezero.adapter import Adapter


class TestBluezero(dbusmock.DBusTestCase):

    @classmethod
    def setUpClass(klass):
        klass.start_session_bus()
        klass.start_system_bus()
        klass.dbus_con = klass.get_dbus(True)

    def setUp(self):
        # bluetoothd
        (self.p_mock, self.obj_bluez) = self.spawn_server_template(
            'bluez5', {}, stdout=subprocess.PIPE)
        self.dbusmock_bluez = dbus.Interface(self.obj_bluez, 'org.bluez.Mock')
        # Set up an adapter and device.
        adapter_name = 'hci0'
        device_address = '11:22:33:44:55:66'
        device_alias = 'My Phone'

        ml = GLib.MainLoop()

        self.dbusmock_bluez.AddAdapter(adapter_name, 'my-computer')

    def tearDown(self):
        self.p_mock.terminate()
        self.p_mock.wait()

    def test_adapter_address(self):
        dongle = Adapter()
        self.assertEqual(dongle.address(), '00:01:02:03:04:05')

    def test_adapter_name(self):
        dongle = Adapter()
        self.assertEqual(dongle.name(), 'my-computer')

    def test_adapter_alias(self):
        dongle = Adapter()
        self.assertEqual(dongle.alias(), 'my-computer')

    def test_adapter_alias_write(self):
        dev_name = 'my-test-dev'
        dongle = Adapter()
        dongle.alias(dev_name)
        self.assertEqual(dongle.alias(), dev_name)

    def test_adapter_power(self):
        dongle = Adapter()
        self.assertEqual(dongle.powered(), 1)

    def test_adapter_power_write(self):
        dongle = Adapter()
        dongle.powered(0)
        self.assertEqual(dongle.powered(), 0)

    def test_adapter_discoverable(self):
        dongle = Adapter()
        self.assertEqual(dongle.discoverable(), 1)

    def test_adapter_discoverabletimeout(self):
        dongle = Adapter()
        self.assertEqual(dongle.discoverabletimeout(), 180)

    def test_adapter_pairable(self):
        dongle = Adapter()
        self.assertEqual(dongle.pairable(), 1)

    def test_adapter_pairabletimeout(self):
        dongle = Adapter()
        self.assertEqual(dongle.pairabletimeout(), 180)

    def test_adapter_discovering(self):
        dongle = Adapter()
        self.assertEqual(dongle.discovering(), 1)

if __name__ == '__main__':
    # avoid writing to stderr
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout,
                                                     verbosity=2))
