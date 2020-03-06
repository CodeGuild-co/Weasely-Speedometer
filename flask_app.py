from police_api import PoliceAPI
from flask import Flask, render_template, request
import math
app = Flask(__name__)

@app.route('/', methods=['GET'])
def location():

    return render_template("map.html")

@app.route('/', methods=['POST'])
def latlng():
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    api = PoliceAPI()
    n = api.locate_neighbourhood(lat, lng)
    ncrimes=len(api.get_crimes_area(n.boundary, date='2020-01'))
    population= n.population
    highRisk = False

    if population > 0:
        cpp= ncrimes/population
        noMonths = 1/cpp
        noMonths = round(noMonths)
        Mth = str(noMonths)
    else:
        minLat = min(latlong[0] for latlong in n.boundary)
        maxLat = max(latlong[0] for latlong in n.boundary)
        minLong = min(latlong[1] for latlong in n.boundary)
        maxLong = max(latlong[1] for latlong in n.boundary)
        totalLat = maxLat - minLat
        totalLong = maxLong - minLong
        latMeters = totalLat * 111.32
        longCos = math.cos(totalLong)
        longMeters = (longCos/360)*40075
        totalArea = latMeters * longMeters
        ukArea = 242495
        numberPeople = 66440000
        ppa = numberPeople/ukArea
        ppn = totalArea*ppa
        ppn = round(ppn)
        cpp= ncrimes/ppn
        noMonths = 1/cpp
        noMonths = round(noMonths)
        Mth = str(noMonths)
        population = ppn
    if cpp>0.02:
        highRisk = True
    #as = Antisocial behaviour
    #t = theft
    #b = burglary
    #cda = criminal damage and arson
    #d = drugs
    #pw = possession of weapons
    #po = public order
    #r = robbery
    #s = shoplifting
    #vc = vehicle crime
    #vso = violent and sexual offences
    #o = other crime
    asTally = 0
    tTally = 0
    bTally = 0
    cdaTally = 0
    dTally = 0
    pwTally = 0
    poTally = 0
    rTally = 0
    sTally = 0
    vcTally = 0
    vsoTally = 0
    oTally = 0
    crimes = api.get_crimes_area(n.boundary, date='2020-01')
    for x in crimes:
        type = str(x.category)
        if type == '<CrimeCategory> Anti-social behaviour':
            asTally += 1
        elif type == '<CrimeCategory> Bicycle theft' or type == '<CrimeCategory> Other theft' or type == '<CrimeCategory> Theft from the person':
            tTally += 1
        elif type == '<CrimeCategory> Burglary':
            bTally += 1
        elif type == '<CrimeCategory> Criminal damage and arson':
            cdaTally += 1
        elif type == '<CrimeCategory> Drugs':
            dTally += 1
        elif type == '<CrimeCategory> Possession of weapons':
            pwTally += 1
        elif type == '<CrimeCategory> Public order':
            poTally += 1
        elif type == '<CrimeCategory> Robbery':
            rTally += 1
        elif type == '<CrimeCategory> Shoplifting':
            sTally += 1
        elif type == '<CrimeCategory> Vehicle crime':
            vcTally += 1
        elif type == '<CrimeCategory> Violence and sexual offences':
            vsoTally += 1
        elif type == '<CrimeCategory> Other crime':
            oTally += 1
        array = [asTally, tTally, bTally, cdaTally, dTally, pwTally, poTally, rTally, sTally, vcTally, vsoTally, oTally]
        array.sort(reverse=True)
        mostCrimeNumber = int(array[0])


    if array[0] == bTally:
        mostCrime = 'Burglary'
    elif array[0] == cdaTally:
        mostCrime = 'Criminal damage and arson'
    elif array[0] == dTally:
        mostCrime = 'Drugs'
    elif array[0] == pwTally:
        mostCrime = 'Possession of weapons'
    elif array[0] == poTally:
        mostCrime = 'Public order'
    elif array[0] == rTally:
        mostCrime = 'Robbery'
    elif array[0] == sTally:
        mostCrime = 'Shoplifting'
    elif array[0] == vcTally:
        mostCrime = 'Vehicle crime'
    elif array[0] == vsoTally:
        mostCrime = 'Violence and sexual offences'
    elif array[0] == oTally:
        mostCrime = 'Other crime'
    elif array[0] == asTally:
        mostCrime = 'Antisocial Behaviour'

    #these are the percentages that the clock needs:
    asTotal = (asTally/ncrimes)*100
    tTotal = (tTally/ncrimes)*100
    bTotal = (bTally/ncrimes)*100
    cdaTotal = (cdaTally/ncrimes)*100
    dTotal = (dTally/ncrimes)*100
    pwTotal = (pwTally/ncrimes)*100
    poTotal = (poTally/ncrimes)*100
    rTotal = (rTally/ncrimes)*100
    sTotal = (sTally/ncrimes)*100
    vcTotal = (vcTally/ncrimes)*100
    vsoTotal = (vsoTally/ncrimes)*100
    oTotal = (oTally/ncrimes)*100


    return render_template(
        'clock.html',
        lng=lng,
        lat=lat,
        ncrimes=ncrimes,
        n=n,
        mostCrime=mostCrime,
        mostCrimeNumber=mostCrimeNumber,
        Mth=Mth,
        highRisk=highRisk,
        population=population,
        asTotal=asTotal,
        tTotal=tTotal,
        bTotal=bTotal,
        cdaTotal=cdaTotal,
        dTotal=dTotal,
        pwTotal=pwTotal,
        poTotal=poTotal,
        rTotal=rTotal,
        sTotal=sTotal,
        vcTotal=vcTotal,
        vsoTotal=vsoTotal,
        oTotal=oTotal,
        )

