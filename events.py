# This file packages all events into a binary file, which will be a part of the
# catalog file.
from struct import *
import csv
from common import *

def event_pack(event):
    header = pack(">xxBxHHHIHH", event['domain'], event['record_byte_offset'],
                  event['record_length'], event['counter_offset'],
                  event['flag'], event['primary_group_index'],
                  event['group_count'])

    e = header + pack_text(event['name']) + pack_text(event['description'])
    e += pack_text(event['detailed_description'])

    return pad16(e)

def pack_events(events_csv):
    events = ""

    with open(events_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        event = {}
        count = 0
        for row in reader:
            count += 1
            event['domain'] = int(row['domain'])
            event['record_byte_offset'] = int(row['record byte offset'])
            event['record_length'] = int(row['record length'])
            event['counter_offset'] = int(row['counter offset'])
            event['flag'] = int(row['flag'])
            event['primary_group_index'] = int(row['primary group index'])
            event['group_count'] = int(row['group count'])
            event['name'] = row['name']
            event['description'] = row['description']
            event['detailed_description'] = row['detailed description']

            events += event_pack(event)

        return pad_page(events, PAGE_SIZE), count

if __name__ == "__main__":
    events = pack_events('events.csv')
    if len(events) == 0:
        print "Error in generating events binary dump"

    f = open('events.bin', 'w')
    f.write(events)
    f.close()
    hexdump(events, " ", 16)
