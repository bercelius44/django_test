from core.models import DriverRecord
import requests

def update_drivers_location():
    print("Updating drivers status")
    j = requests.get("https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json").json()
    for i in j["alfreds"]:
        try:
            driver = DriverRecord.objects.get(pk=i["id"])
            driver.location = i["lat"] + "," + i["lng"]
            driver.date = i['lastUpdate']
            driver.save()
        except DriverRecord.DoesNotExist:
            driver = DriverRecord(pk = i["id"], location = i["lat"] + "," + i["lng"], date=i['lastUpdate'])
            driver.save()
 
        