import requests

cookies = {
    '__cf_bm': 'Bj.sFqM3t5VlweBXfNy4TaCbRhlp6FsR8BghvasqUgE-1755944153-1.0.1.1-vMcfN62Z7R3Ha1Aj.lITbZ3SsfjAZ.B1MwiZ1lyaIyaJqf5NhYNkVxMUHrFwcCjHlY01yxyXbTY6tIwoIovmw1fH9eCrDjvuSHbm50d8t6Y',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': '68BE8F88-7CD2-4890-A24C-96E20E4EF9EE',
    'x-careem-beta': 'false',
    # 'cookie': '__cf_bm=Bj.sFqM3t5VlweBXfNy4TaCbRhlp6FsR8BghvasqUgE-1755944153-1.0.1.1-vMcfN62Z7R3Ha1Aj.lITbZ3SsfjAZ.B1MwiZ1lyaIyaJqf5NhYNkVxMUHrFwcCjHlY01yxyXbTY6tIwoIovmw1fH9eCrDjvuSHbm50d8t6Y',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': '68BE8F88-7CD2-4890-A24C-96E20E4EF9EE',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '55.29878677233094',
    'x-careem-appengine-page-session-id': '8c3d87ea-410f-4865-85af-f81a5418074b',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.25429866282875,55.29878677233094',
    'x-careem-appengine-api-version': '2025-07-07',
    'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTk1MTE4OCwiaWF0IjoxNzU1ODY0Nzg4LCJqdGkiOiIzMzVkNTQ2OC1jNDk2LTRmY2MtYTNiZS1lNDIzYTA2MDI5NGYifQ.naeAHsgNBesdMYKGVAsUsEzKOuuyORO6_G_0un9czEMRISPRHXquIPi2bE8GfCiU9HHrsLEy7fpbNgCKyxRHQrmIU5SLJJDLU9EEy38KBNA89nHv-fmEDOWl5ZdUa-56dfk1JRW7-qYXlqDKibxnf109fjvfF5fuAonWNyZ_a4PPwmyEF1PgR2q4NgToIV2PE2HHsqrZ46wdrLLdYsGieRnYFYz_hQVVOlFUkgrKMnjL3Mrer4aCIIpArGYKbOKu8VUBhYkAgsi9ogbZRxyvgpYWF396zxzlHs2tV-IZVqk9Fxul2328-U5YOKTEfhqxIV1OkSbwBEjxDhjJvZOHbg',
    'x-careem-operating-system': 'iOS/18.6.1',
    'x-careem-permissions': 'location:granted',
    'accept-language': 'en',
    'lat': '25.25429866282875',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

params = {
    'selectedServiceAreaId': '0',
    'refreshCounter': '3',
}

response = requests.get(
    'https://appengine.careemapis.com/v1/page/ea-discovery-home',
    params=params,
    cookies=cookies,
    headers=headers,
)