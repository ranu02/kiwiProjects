import boto3

# Marshmallow example
import os

from dynamorm import DynaModel

from marshmallow import fields, validate, validates, ValidationError

from django.views.generic import TemplateView, View
from schematics import types

from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute


import datetime

from dynamorm import DynaModel, GlobalIndex, ProjectAll

# In this example we'll use Marshmallow, but you can also use Schematics too!
# You can see that you have to import the schema library yourself, it is not abstracted at all
from marshmallow import fields


class Makedir11111111111111(TemplateView):
    """
    Views used  for User Registration Success page
    """
    template_name = 'index.html'

    def get(self, request, **kwargs):
        """
        Method to load login page
        :param kwargs: keyword argument
        :param request: request argument dict type
        :return:Sign up success page
        """
        dynamodb = boto3.resource('dynamodb')
        abc = list(dynamodb.tables.all())
        abc


# Our objects are defined as DynaModel classes
class Thing(DynaModel):
    class Table:
        name = 'dev-things'
        hash_key = 'id'
        read = 5
        write = 1

    class Schema:
        id = fields.String(required=True)
        name = fields.String()
        color = fields.String(validate=validate.OneOf(('purple', 'red', 'yellow')))
        compound = fields.Dict(required=True)

        @validates('name')
        def validate_name(self, value):
            # this is a very silly example just to illustrate that you can fill out the
            # inner Schema class just like any other Marshmallow class
            if self.name.lower() == 'evan':
                raise ValidationError("No Evan's allowed")

    def say_hello(self):
        thing = Thing(id="thing1", name="Thing One", color="purple")
        thing.save()



class UserModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = "dynamodb-user1"

    email = UnicodeAttribute(null=True)
    first_name = UnicodeAttribute(range_key=True)
    last_name = UnicodeAttribute(hash_key=True)


def say_hello():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)




class Location(MapAttribute):

    lat = NumberAttribute(attr_name='latitude')
    lng = NumberAttribute(attr_name='longitude')
    name = UnicodeAttribute()
    # class Meta:
    #     table_name = "dynamodb_location"


class Person(MapAttribute):

    fname = UnicodeAttribute(attr_name='firstName')
    lname = UnicodeAttribute()
    age = NumberAttribute()
    # class Meta:
    #     table_name = "dynamodb_person"


class OfficeEmployeeMap(MapAttribute):

    office_employee_id = NumberAttribute()
    person = Person()
    office_location = Location()
    # class Meta:
    #     table_name = "dynamodb_office_emp"


class Thread(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "Thread"
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    answered = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute(null=True)




class Office(Model):
    class Meta:
        table_name = 'OfficeModel'

    office_id = NumberAttribute(hash_key=True)
    address = Location()
    employees = ListAttribute(of=OfficeEmployeeMap)


class Makedir(TemplateView):
    """
    Views used  for User Registration Success page
    """
    template_name = 'index.html'

    def get(self, request, **kwargs):
        """
        Method to load login page
        :param kwargs: keyword argument
        :param request: request argument dict type
        :return:Sign up success page
        """
        # abc = UserModel.create_table(read_capacity_units=1, write_capacity_units=1)

        # abc1 = Office.create_table(read_capacity_units=1, write_capacity_units=1)
        # abc2 = Person.create_table(read_capacity_units=1, write_capacity_units=1)
        # abc3 = OfficeEmployeeMap.create_table(read_capacity_units=1, write_capacity_units=1)
        # abc4 = Office.create_table(read_capacity_units=1, write_capacity_units=1)

        # Create the table
        # if not Thread.exists():
        #     abc1 = Thread.create_table(wait=True)

        thread_item = Thread(
            'Some Forum',
            'Some Subject',
            tags=['foo', 'bar'],
            last_post_datetime=datetime.datetime.now()
        )

        # try:
        #     Thread.get('does not', 'exist')
        # except Thread.DoesNotExist:
        #     pass

        # Save the thread
        abc1 = thread_item.save()
        abc1



