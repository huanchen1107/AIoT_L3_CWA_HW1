"""Probe township-level datasets F-D0047-001 to F-D0047-007."""
import os, requests, urllib3
from dotenv import load_dotenv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
API_KEY = os.getenv("CWA_API_KEY")
BASE = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"

for dsnum in range(1, 12, 2):  # odd numbers: 001, 003, 005, 007, 009, 011
    ds = f"F-D0047-{dsnum:03d}"
    r = requests.get(f"{BASE}/{ds}",
        params={"Authorization": API_KEY, "format": "JSON", "limit": 1},
        timeout=15, verify=False)
    if r.ok:
        d = r.json()
        recs = d.get("records", {})
        locs_list = recs.get("Locations", [])
        if locs_list:
            group = locs_list[0]
            lname = group.get("LocationsName")
            districts = group.get("Location", [])
            elems = []
            if districts:
                elems = [e.get("ElementName") for e in districts[0].get("WeatherElement", [])]
                times = districts[0]["WeatherElement"][0].get("Time", []) if districts[0].get("WeatherElement") else []
            print(f"[OK] {ds} LocationsName={lname} districts={len(districts)} elems={elems[:4]} periods={len(times)}")
        else:
            print(f"[OK] {ds} records_keys={list(recs.keys())}")
    else:
        print(f"[XX] {ds} HTTP {r.status_code}")
