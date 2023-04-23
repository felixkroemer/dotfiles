import requests
import os
import time
from dotenv import load_dotenv
import datetime
import subprocess

load_dotenv()

jsessionid = requests.get("https://" + os.getenv("HOST")).cookies["JSESSIONID"]

data = {
    "bibLoginLayer.number": os.getenv("NUMBER"),
    "bibLoginLayer.password": os.getenv("PASSWORD"),
    "bibLoginLayer.terms_cb": "1",
    "bibLoginLayer.terms": "1",
    "bibLoginLayer.gdpr_cb": "1",
    "bibLoginLayer.gdpr": "1",
    "eventHandler": "loginClicked",
    "state": "rO0ABXNyABdjb20uZ2VuaW9zLkJpYkxvZ2luRm9ybQAAAAAAAAABAgACWgALbm90Q2xvc2FibGVMAAZhY3Rpb250ACBMY29tL2dlbmlvcy9SdW5uYWJsZUZvcm1GYWN0b3J5O3hyABljb20uZ2VuaW9zLmphc3R5LkJhc2VGb3JtAAAAAAAAAAECAAFMAA5yZW5kZXJpbmdTdHlsZXQAEkxqYXZhL2xhbmcvU3RyaW5nO3hyABNjb20uamFzdHkuY29yZS5Gb3JtAAAAAAAAAAECAAJJABNsYXN0QXNzaWduZWRDaGlsZElkTAAGYmFzZUlkcQB+AAN4cgAYY29tLmphc3R5LmNvcmUuQ29tcG9uZW50AAAAAAAAAAECAAhaAAd2aXNpYmxlTAAFY2xhenpxAH4AA0wABGRhdGFxAH4AA0wABWRhdGEycQB+AANMAAVkYXRhM3EAfgADTAAOZGF0YUF0dHJpYnV0ZXN0AA9MamF2YS91dGlsL01hcDtMAAVzdHlsZXEAfgADTAAFdGl0bGVxAH4AA3hyAB1jb20uamFzdHkuY29yZS5Db21wb25lbnRQcm94eQAAAAAAAAABAgABTAACaWRxAH4AA3hwdAANYmliTG9naW5MYXllcgFwcHBwcHBwAAAAAXEAfgAJcAFzcgAXY29tLmdlbmlvcy5SZWxvYWRBY3Rpb24AAAAAAAAAAQIAAHhw",
}
genios_auth = requests.post("https://" + os.getenv("HOST") + "/formEngine/doAction", data=data, cookies={"JSESSIONID": jsessionid}).cookies["GeniosAuth"]

cookies = {"JSESSIONID": jsessionid, "Genios-Auth": genios_auth}
today = datetime.datetime.today()
while today.weekday() >= 5:
    today = today - datetime.timedelta(days=1)
year = today.year
month = '{:02d}'.format(today.month)
day = '{:02d}'.format(today.day)
url = "https://" + os.getenv("HOST") + "/stream/dbBoundFileConsole"
requests.post(url, data={"id": "HB__:{year}:{day}{month}{year}".format(year=year, month=month, day=day),
                         "fileName": "HB/HEFTE/HB_{year}_{day}{month}{year}.pdf".format(year=year, month=month, day=day)}, cookies=cookies)
url = "https://" + os.getenv("HOST") + "/stream/dbBoundFile?id=HB__:{year}:{day}{month}{year}&fileName=HB%2FHEFTE%2FHB_{year}_{day}{month}{year}.pdf".format(year = year, month = month, day= day)
pdf = requests.get(url, cookies=cookies)

if pdf.status_code != 200:
    print("Error {}".format(pdf.status_code))
else:
    path = os.path.join(os.environ["HOMEPATH"], "Desktop", "HB_{}.{}.{}.pdf".format(day, month, year))
    with open(path, "wb") as f:
        f.write(pdf.content)
    subprocess.Popen([path], shell=True)
