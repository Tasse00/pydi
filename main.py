import logging

import di
from di.decorator import bean, register_group



class PartA:
    pass


class PartB:
    def __init__(self, a: PartA):
        self.a = a

@bean
class PartC:
    def __init__(self, a: PartA):
        self.a = a


@bean(id="app1", consts={"ss": "111"})
@bean(id="app2", consts={"ss": "222"})
@bean(id="app3", consts={"ss": "333"})
class PartD:
    def __init__(self, a: PartA, b: PartB, c: PartC, ss: str = "SSS"):
        self.a = a
        self.b = b
        self.c = c
        self.ss = ss

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    ctx = di.NewContext()

    register_group(ctx)

    print(ctx.beans_xml)

    #
    # ctx.register(PartD, id="app1", consts={'ss': '111'})
    # ctx.register(PartD, id="app2", consts={'ss': '222'})
    # ctx.register(PartD, id="app3")
    # ctx.register(PartC)
    # ctx.register(PartB)
    # ctx.register(PartA)
    #
    # print(ctx.beans_xml)
    #
    # app1: PartD = ctx.instance_by_id('app1')
    # app2: PartD = ctx.instance_by_id('app2')
    # app3: PartD = ctx.instance_by_id('app3')
    #
    # assert (app1.a == app1.b.a == app1.c.a == app2.a == app2.b.a == app2.c.a)
    #
    # assert app1 is ctx.instance_by_id('app1')
    # assert app2 is ctx.instance_by_id('app2')
    # assert app3 is ctx.instance_by_id('app3')
    #
    # assert app1 is not app2
    #
    # assert app1.ss == "111"
    # assert app2.ss == "222"
    # assert app3.ss == "SSS"
