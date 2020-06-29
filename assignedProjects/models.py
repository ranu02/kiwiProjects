
"""
An example using Amazon's Thread example for motivation
http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SampleTablesAndData.html
"""
from __future__ import print_function
import logging
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)
from datetime import datetime

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True


class ThreadMy(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "ThreadMy"
    forum_name = UnicodeAttribute(hash_key=True)
    subject = UnicodeAttribute(range_key=True)
    views = NumberAttribute(default=0)
    replies = NumberAttribute(default=0)
    answered = NumberAttribute(default=0)
    tags = UnicodeSetAttribute()
    last_post_datetime = UTCDateTimeAttribute(null=True)

# Delete the table
# print(Thread.delete_table())

# Create the table
if not ThreadMy.exists():
    ThreadMy.create_table(wait=True)

