import unittest
from pathlib import Path

from di import NewContext
from di.ref import IdRef
from tests.app import Restaurant, Kitchen, Cashier, EatingRoom, Staff
from tests.app.seat import Seat


class TestContext(unittest.TestCase):

    xml_file: Path = Path(__file__).parent.joinpath("resources", "beans.xml")

    def test_register(self):
        ctx = NewContext()
        ctx.register(Restaurant, id="rest", refs={"manager": IdRef('manager-staff')})
        ctx.register(Kitchen, refs={'staff': IdRef('kitchen-staff')})
        ctx.register(Cashier, refs={'staff': IdRef('manager-staff')})
        ctx.register(EatingRoom, refs={'staff': IdRef('eatingroom-staff')})
        ctx.register(Seat)
        ctx.register(Staff, id='kitchen-staff', consts={'name': 'kitchen-staff'})
        ctx.register(Staff, id='eatingroom-staff', consts={'name': 'eatingroom-staff'})
        ctx.register(Staff, id='manager-staff', consts={'name': 'manager-staff'})

        rest: Restaurant = ctx.instance_by_id("rest")

        self.assertEqual(rest.manager.name, 'manager-staff')
        self.assertEqual(rest.kitchen.staff.name, 'kitchen-staff')
        self.assertEqual(rest.kitchen.number, 1)
        self.assertEqual(rest.cashier.staff, rest.manager)
        self.assertEqual(rest.eatingroom.staff.name, 'eatingroom-staff')
        self.assertEqual(rest.eatingroom.seat.id, 'default-seat')

        self.assertEqual(rest, ctx.instance_by_cls(Restaurant))

    def test_register_to_xml(self):
        ctx = NewContext()
        ctx.register(Restaurant, id="rest", refs={"manager": IdRef('manager-staff')})
        ctx.register(Kitchen, refs={'staff': IdRef('kitchen-staff')})
        ctx.register(Cashier, refs={'staff': IdRef('manager-staff')})
        ctx.register(EatingRoom, refs={'staff': IdRef('eatingroom-staff')})
        ctx.register(Seat)
        ctx.register(Staff, id='kitchen-staff', consts={'name': 'kitchen-staff'})
        ctx.register(Staff, id='eatingroom-staff', consts={'name': 'eatingroom-staff'})
        ctx.register(Staff, id='manager-staff', consts={'name': 'manager-staff'})

        self.assertEqual(self.xml_file.read_text(), ctx.format_beans_xml(indent="    "))

    def test_register_file(self):
        ctx = NewContext()
        ctx.register_file(str(self.xml_file))

        rest: Restaurant = ctx.instance_by_id("rest")

        self.assertEqual(rest.manager.name, 'manager-staff')
        self.assertEqual(rest.kitchen.staff.name, 'kitchen-staff')
        self.assertEqual(rest.kitchen.number, 1)
        self.assertEqual(rest.cashier.staff, rest.manager)
        self.assertEqual(rest.eatingroom.staff.name, 'eatingroom-staff')
        self.assertEqual(rest.eatingroom.seat.id, 'default-seat')

        self.assertEqual(rest, ctx.instance_by_cls(Restaurant))

    def test_register_group(self):
        ctx = NewContext()
        ctx.register_group()

        rest: Restaurant = ctx.instance_by_id("rest")

        self.assertEqual(rest.manager.name, 'manager-staff')
        self.assertEqual(rest.kitchen.staff.name, 'kitchen-staff')
        self.assertEqual(rest.kitchen.number, 1)
        self.assertEqual(rest.cashier.staff, rest.manager)
        self.assertEqual(rest.eatingroom.staff.name, 'eatingroom-staff')
        self.assertEqual(rest.eatingroom.seat.id, 'default-seat')

        self.assertEqual(rest, ctx.instance_by_cls(Restaurant))