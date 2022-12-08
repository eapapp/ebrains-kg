import requests as rq
import json

baseurl = "https://core.kg.ebrains.eu/v3-beta/queries/"


def getData(apiurl, headers, scope):
    url = apiurl + "?stage=" + scope
    resp = rq.get(url, headers=headers)
    data = resp.json()
    return(data)


def sortJSON(unsortedjson):

    names = []
    for i in unsortedjson:
        names.append(i["name"].lower())

    names.sort()

    sortedjson = []

    for n in names:
        for d in unsortedjson:
            if d["name"].lower()==n:
                sortedjson.append(d)

    return(sortedjson)


def getControlledTerms(headers,scope,filename,queryID):

    terms = []
    apiurl = baseurl + queryID + "/instances"   
    results = getData(apiurl=apiurl, headers=headers, scope=scope)["data"] 

    for r in results:
        item = {}
        for i in r["https://schema.hbp.eu/myQuery/identifier"]:
            if i.startswith('https://kg.ebrains.eu/api/instances/'):    # 'https://openminds.ebrains.eu/'                
                item["identifier"] = i

        item["name"] = r["https://schema.hbp.eu/myQuery/name"]

        if "https://schema.hbp.eu/myQuery/species" in r.keys():
            for sid in r["https://schema.hbp.eu/myQuery/species"][0]["https://schema.hbp.eu/myQuery/identifier"]:
                if sid.startswith('https://kg.ebrains.eu/api/instances/'): break

            item["species"] = {"identifier": sid,
                               "name": r["https://schema.hbp.eu/myQuery/species"][0]["https://schema.hbp.eu/myQuery/name"]}

        terms.append(item)

    terms = sortJSON(terms)

    with open(filename + ".json","w") as f:
        json.dump(obj=terms,fp=f,indent=2, sort_keys=True)



if __name__=='__main__':
    # Fetch controlled terms from the KG v3 and save as .json for the metadata wizard
    # Note: keywords are not yet in place, query to be extended

    print("\nFetch controlled terms from the KG v3 and save as .json for the metadata wizard\n---")
    token = input("KG token: ")

    headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + token
        }

    scope="RELEASED"    # IN_PROGRESS

    queries = {"preparationType":"3a2d25f8-891a-4691-90ba-d668da5540e6",
               "technique":"fcb0ef51-1496-4cfb-9629-f229c011cbfa",
               "experimentalApproach":"b1695c78-63ba-4074-bd06-faefb8502b56",
               "semanticDataType":"d4c3f650-c04c-49f7-8961-c3ca515b4aff",
               "biologicalSex":"52ded04b-6e3a-47d8-a60d-beb00ab99454",
               "ageCategory":"b6c5d138-4695-4740-b969-0805a7ff4f40",
               "species":"96394f81-d536-46cd-adbf-eeb0499ddfbe",
               "strain":"6ed01e7c-6245-4a7f-95c3-4fa412c00770"
                }

    for q in queries.keys():
        getControlledTerms(headers,scope,q,queries[q])
