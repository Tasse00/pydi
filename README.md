# Simple-PyDI

## Intro

simple python dependency injection framwork

just like java spring-framework. 

## Install

```shell script
pip install simple-pydi
```

## Usage

### Components

app.py
``` python
class Engine:
    pass


class Wheels:
    def __init__(self, wheels_count: int = 4):
        self.wheels_count = wheels_count


class Body:
    pass


class Person:
    def __init__(self, name: str):
        self.name = name


class Car:
    def __init__(self, engine: Engine, wheels: Wheels, body: Body, driver: Person):
        self.engine = engine
        self.wheels = wheels
        self.body = body
        self.driver = driver

```

### Direct Register

main.py
```python
from di import NewContext

from app import Car, Engine, Wheels, Body, Person


ctx = NewContext()

# directly register beans
ctx.register(Car, id='car')
ctx.register(Engine)
ctx.register(Wheels)
ctx.register(Body)
ctx.register(Person, consts={'name': 'Ben'})

car: Car = ctx.instance_by_id('car')

assert car.driver.name == 'Ben'
assert car.wheels.wheels_count == 4

# view beans xml definition
print(ctx.format_beans_xml())
```

### Register by XML File

beans.xml
```xml
<?xml version="1.0" ?>
<beans>
	<bean cls="app.Car" id="car" singleton="true">
		<property name="engine" ref="cls:app.Engine"/>
		<property name="wheels" ref="cls:app.Wheels"/>
		<property name="body" ref="cls:app.Body"/>
		<property name="driver" ref="cls:app.Person"/>
	</bean>
	<bean cls="app.Engine" id="app.Engine" singleton="true"/>
	<bean cls="app.Wheels" id="app.Wheels" singleton="true">
		<property name="wheels_count" value="4" value-type="int"/>
	</bean>
	<bean cls="app.Body" id="app.Body" singleton="true"/>
	<bean cls="app.Person" id="app.Person" singleton="true">
		<property name="name" value="Ben" value-type="str"/>
	</bean>
</beans>
```

main.py
```python
from di import NewContext

from app import Car


ctx = NewContext()

# get beans definition from xml file
ctx.register_file('beans.xml')

car: Car = ctx.instance_by_id('car')

assert car.driver.name == 'Ben'
assert car.wheels.wheels_count == 4

# view beans xml definition
print(ctx.format_beans_xml())
```

### Use Decorator Definition

app.py
```python
from di.decorator import bean


@bean
class Engine:
    pass


@bean
class Wheels:
    def __init__(self, wheels_count: int = 4):
        self.wheels_count = wheels_count


@bean
class Body:
    pass


@bean(consts={'name': 'Ben'})
class Person:
    def __init__(self, name: str):
        self.name = name


@bean(id='car')
class Car:
    def __init__(self, engine: Engine, wheels: Wheels, body: Body, driver: Person):
        self.engine = engine
        self.wheels = wheels
        self.body = body
        self.driver = driver
```

main.py
```python
from di import NewContext

from app import Car

ctx = NewContext()

# register pre defined group (by decorator) 
ctx.register_group()

car: Car = ctx.instance_by_cls(Car)

assert car.driver.name == 'Ben'
assert car.wheels.wheels_count == 4

# view beans xml definition
print(ctx.format_beans_xml())
```
