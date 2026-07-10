"""Regenerate a coherent demo dataset.
Flight status and disruption events are generated together so the UI, agents and passenger view stay in sync.
"""
import json, random
from faker import Faker
from pathlib import Path

random.seed(42); fake=Faker(); Faker.seed(42)
BASE=Path(__file__).resolve().parent
weather={
    "JFK":{"condition":"Thunderstorm","visibility_miles":1.2,"wind_knots":35,"severity":"HIGH"},
    "LAX":{"condition":"Clear","visibility_miles":10.0,"wind_knots":8,"severity":"LOW"},
    "ORD":{"condition":"Snow","visibility_miles":2.5,"wind_knots":22,"severity":"MEDIUM"},
    "DFW":{"condition":"Clear","visibility_miles":9.0,"wind_knots":12,"severity":"LOW"},
    "ATL":{"condition":"Fog","visibility_miles":0.8,"wind_knots":5,"severity":"HIGH"},
}
origins=list(weather); destinations=["MIA","SEA","BOS","DEN","LAS"]
statuses=["On Time"]*10+["Delayed"]*6+["Cancelled"]*4
random.shuffle(statuses)
flights=[]; disruptions={}
for i,status in enumerate(statuses):
    fid=f"AA{120+i*37}"
    origin=random.choice(origins); destination=random.choice(destinations)
    flight={"flight_id":fid,"origin":origin,"destination":destination,
            "scheduled_departure":f"2026-07-07T{random.randint(6,22):02d}:{random.choice(['00','15','30','45'])}:00",
            "aircraft":random.choice(["Boeing 737","Airbus A320","Boeing 777"]),"passengers":random.randint(80,280),"status":status}
    flights.append(flight)
    if status!="On Time":
        w=weather[origin]
        if w['severity']=='HIGH' and w['condition']=='Thunderstorm': cause='Severe Thunderstorm'
        elif w['severity']=='HIGH' and w['condition']=='Fog': cause='Dense Fog'
        elif w['condition']=='Snow': cause='Heavy Snow'
        else: cause=random.choice(['Mechanical Issue','ATC Hold','Ground Stop','Crew Shortage'])
        delay=random.randint(35,150) if status=='Delayed' else random.choice([0,190,210])
        disruptions[fid]={"event_active":True,"status":status,"affected_airport":origin,"cause":cause,
            "event_start":"2026-07-07T08:00:00","current_delay_minutes":delay,"severity":w['severity'],
            "recovery_required":True,"escalation_threshold_minutes":180}
crew=[{"crew_id":f"CR{i+1:03d}","name":fake.name(),"role":random.choice(["Captain","First Officer","Flight Attendant"]),
       "available":random.choice([True,True,True,False]),"base":random.choice(origins),"hours_remaining":random.randint(2,12)} for i in range(30)]
gates={a:[{"gate":f"{a}-{chr(65+i)}{j}","available":random.choice([True,False])} for i in range(3) for j in range(1,6)] for a in origins}
for name,data in [('flights.json',flights),('weather.json',weather),('crew.json',crew),('gates.json',gates),('disruptions.json',disruptions)]:
    (BASE/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
print('Coherent mock data generated successfully.')
