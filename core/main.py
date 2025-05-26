import orgparse as org
# from from c0rHash import labelHash
from datetime import datetime
import json
from uuid import uuid4

def assign(item, tasker='Generic_Tasker') -> None:
    print(f"Item: {item} -> Tasker: {tasker}")

# 1. load the primary capture endpoint
root = org.load('/home/ben/workbench/org/inbox.org')

# 2. Loop through each item in the inbox
for entry in root[1:]:
    # 3. check for items that are new or extant 
    props = entry.properties # returns a dict

    # decide if new or not
    if 'ID' not in props:

        # it's a new item -> Generate an ide
        new_id = str(uuid4())
        created_ts = datetime.now().isoformat()

        entry.set_property('ID', new_id)
        entry.set_property('CREATED', created_ts)

        print(f"🆕 Wrote MetaData for '{entry.heading}': ID={new_id}")

    # 5. Assign item to Tasker (worker)
    assign(entry, tasker)

# 6. Commit changes 
root.save() 
