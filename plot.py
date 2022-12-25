from datetime import datetime
import re
from typing import NamedTuple, List
from dateutil.parser import isoparse
import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter

class LogEntry(NamedTuple):
    adr: str
    time: datetime
    cmd: int

class DataSerie(NamedTuple):
    adr: str
    x: List[int]
    y: List[int]

def readlog():
    logentries=[]
    with open("log.txt") as logfile:
        for line in logfile.readlines():
            groups = re.match(r"Time: (?P<Time>.*?) Msg: (?P<Msg>.*?) Adr: (?P<Adr>.*?) Cmd: (?P<Cmd>.*?) Seq: (?P<Seq>.*?) Sum: (?P<Sum>.*?)\n", line).groupdict()
            if groups:
                logentries.append(groups)
    return logentries

def parselog(logentries):
    parsedentries=[]
    for entry in logentries:
        parsed=LogEntry(
            adr=entry['Adr'],
            time=isoparse(entry['Time']),
            cmd=int(entry['Cmd'].split(" ")[0], 16)
        )
        parsedentries.append(parsed)
    return parsedentries

def plot(dataseries):
    fig, axs = plt.subplots(len(dataseries), sharex=True)

    i=0
    for serie in dataseries:
        axs[i].step(serie.x, serie.y, where='post', label=serie.adr)
        axs[i].legend(loc="upper right")
        axs[i].set_ylim([0, 5])
        i+=1

    plt.grid(axis='x', color='0.95')
    plt.show()

def get_field(field, data):
    return list(map(lambda d: getattr(d, field), data))

def filteradr(parsedentries):
    adrs=set()
    for parsed in parsedentries:
        adrs.add(parsed.adr)
    return adrs

def convert_to_dataseries(parsedentries):
    adrs=filteradr(parsedentries)

    dataseries=[]
    for adress in filteradr(parsedentries):
        entry=DataSerie(
            adr=adress,
            x=get_field('time', filter(lambda e: e.adr == adress, parsedentries)),
            y=get_field('cmd', filter(lambda e: e.adr == adress, parsedentries)),
        )
        dataseries.append(entry)
    return dataseries

def create_sum_series(parsedentries):
    x=[]
    y=[]
    rolling_set=set()

    for parsed in parsedentries:
        x.append(parsed.time)
        if parsed.cmd == 0:
            rolling_set.discard(parsed.adr)
        else:
            rolling_set.add(parsed.adr)
        y.append(len(rolling_set))

    return DataSerie("all", x, y)

logentries = readlog()
parsedentries = parselog(logentries)
dataseries=convert_to_dataseries(parsedentries)

all_series=create_sum_series(parsedentries)

dataseries.append(all_series)
print(dataseries)
plot(dataseries)