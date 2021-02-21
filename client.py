"""
Trivial client to fill the queue with messages.
"""

import sys
from requests.exceptions import ConnectionError as ConnErr
import requests

TEXT="""
It's a mystery to me
The game commences
For the usual fee
Plus expenses
Confidential information,
It's in a diary
This is my investigation,
It's not a public inquiry
I go checking out the reports
Digging up the dirt
You get to meet all sorts
In this line of work
Treachery and treason,
There's always an excuse for it
And when I find the reason
I still can't get used to it
And what have you got at the end of the day?
What have you got to take away?
A bottle of whisky and a new set of lies
Blinds on a window and a pain behind the eyes
Scarred for life
No compensation
Private investigations
"""

stats = {'ConnErr':0}

while True:
    for line in TEXT.splitlines():
        payload = {'body': line}
        try:
            r = requests.post("http://127.0.0.1:5000/api/message", json=payload)
            if stats.get(r.status_code):
                stats[r.status_code] += 1
            else:
                stats[r.status_code] = 1
        except ConnErr:
            stats['ConnErr'] += 1
        except KeyboardInterrupt:
            sys.exit()

    print(stats)
