import requests
from bs4 import BeautifulSoup
# ...existing code...

cookies = {
    '__cf_bm': 'kOoYnDiW5KtsK.RTeSuIFDwRXH8Ncf_q80o1cWhUnD4-1755943042-1.0.1.1-QpuaUs.kbqGpH6flXk.5wdgi7iToKESlvMXFNl7YuU_dMlE.fN6dF4r.EL7wX.YmAkbhEpfTE3gZooaKDUq9lRaBjrYo9pZzMuI0fS6BlPg',
    '_cfuvid': 'MdrlF4KauB8ximZcw6lOfpRTGMuzpwH5X4EEN8L2wJA-1755943042385-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_4_sn_9F6D1610EE1305C89E99576588D5C2CD_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
}

headers = {
    'x-careem-agent': 'ICMA',
    'application': 'careemfood-mobile-v1',
    'x-careem-beta': 'false',
    'session_id': '2597360F-F7AB-4D1D-B70B-B218605F4EB2',
    'user-agent': 'ICMA/25.32.0',
    'x-request-source': 'SUPERAPP',
    # 'cookie': '__cf_bm=kOoYnDiW5KtsK.RTeSuIFDwRXH8Ncf_q80o1cWhUnD4-1755943042-1.0.1.1-QpuaUs.kbqGpH6flXk.5wdgi7iToKESlvMXFNl7YuU_dMlE.fN6dF4r.EL7wX.YmAkbhEpfTE3gZooaKDUq9lRaBjrYo9pZzMuI0fS6BlPg; _cfuvid=MdrlF4KauB8ximZcw6lOfpRTGMuzpwH5X4EEN8L2wJA-1755943042385-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_4_sn_9F6D1610EE1305C89E99576588D5C2CD_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    'x-careem-session-id': '2597360F-F7AB-4D1D-B70B-B218605F4EB2',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '0.0',
    'uuid': '1CF1A6E3-10EC-41CC-A212-B1179014709E',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'meta': 'ios;production;25.32.5 (1);18.6.1;iPhone14,7',
    'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTk1MTE4OCwiaWF0IjoxNzU1ODY0Nzg4LCJqdGkiOiIzMzVkNTQ2OC1jNDk2LTRmY2MtYTNiZS1lNDIzYTA2MDI5NGYifQ.naeAHsgNBesdMYKGVAsUsEzKOuuyORO6_G_0un9czEMRISPRHXquIPi2bE8GfCiU9HHrsLEy7fpbNgCKyxRHQrmIU5SLJJDLU9EEy38KBNA89nHv-fmEDOWl5ZdUa-56dfk1JRW7-qYXlqDKibxnf109fjvfF5fuAonWNyZ_a4PPwmyEF1PgR2q4NgToIV2PE2HHsqrZ46wdrLLdYsGieRnYFYz_hQVVOlFUkgrKMnjL3Mrer4aCIIpArGYKbOKu8VUBhYkAgsi9ogbZRxyvgpYWF396zxzlHs2tV-IZVqk9Fxul2328-U5YOKTEfhqxIV1OkSbwBEjxDhjJvZOHbg',
    'x-careem-operating-system': 'iOS/18.6.1',
    'accept-language': 'en;q=1.0,en;q=0.9',
    'city-id': '1',
    'lat': '0.0',
    'x-careemdomain': 'food',
    'accept': 'application/json',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'device': '389AB7F7-A760-4C92-AE4A-BE96F0DC7BB3',
}

params = {
    'lat': '25.25429940346886',
    'lng': '55.29882889443747',
}

response = requests.get('https://apigateway.careemdash.com/v1/cities/location', params=params, cookies=cookies, headers=headers)

print(response.status_code)
print(response.text)    

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())