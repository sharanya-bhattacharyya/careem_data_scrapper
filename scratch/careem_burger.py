import requests

cookies = {
    '__cf_bm': 'Fe5PV_sHnKfBR4Xm9J.4v3LJa8IzMUYPScOP9XrkVTg-1755945095-1.0.1.1-U.q9SFt_foYLb2A6fhwvjT0WvKV4ggwUtZrNS83qhdhc0iOT3z_fPQFJmPbIxeO9R1kxaiLvn6x6DUKFlQaOWhRPToEj80UvMMcbD1UxXiU',
    '_cfuvid': '2dg21b8utBMcGbFnPFLoxVoW0xZKDAm9HMaxXPDogHg-1755944706603-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_6_sn_9F0556474D97AF03A70B12208CBC52CF_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': '66E13F10-8B37-4367-A418-31306AAC0265',
    'x-careem-beta': 'false',
    # 'cookie': '__cf_bm=Fe5PV_sHnKfBR4Xm9J.4v3LJa8IzMUYPScOP9XrkVTg-1755945095-1.0.1.1-U.q9SFt_foYLb2A6fhwvjT0WvKV4ggwUtZrNS83qhdhc0iOT3z_fPQFJmPbIxeO9R1kxaiLvn6x6DUKFlQaOWhRPToEj80UvMMcbD1UxXiU; _cfuvid=2dg21b8utBMcGbFnPFLoxVoW0xZKDAm9HMaxXPDogHg-1755944706603-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_6_sn_9F0556474D97AF03A70B12208CBC52CF_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    'x-careem-delivery-location': '25.254298691412355,55.298786860924025',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': '66E13F10-8B37-4367-A418-31306AAC0265',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'x-careem-appengine-page-session-id': 'b66bba57-5804-402b-9b08-e0e29cc45180',
    'lng': '55.298786860924025',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.254298691412355,55.298786860924025',
    'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTk1MTE4OCwiaWF0IjoxNzU1ODY0Nzg4LCJqdGkiOiIzMzVkNTQ2OC1jNDk2LTRmY2MtYTNiZS1lNDIzYTA2MDI5NGYifQ.naeAHsgNBesdMYKGVAsUsEzKOuuyORO6_G_0un9czEMRISPRHXquIPi2bE8GfCiU9HHrsLEy7fpbNgCKyxRHQrmIU5SLJJDLU9EEy38KBNA89nHv-fmEDOWl5ZdUa-56dfk1JRW7-qYXlqDKibxnf109fjvfF5fuAonWNyZ_a4PPwmyEF1PgR2q4NgToIV2PE2HHsqrZ46wdrLLdYsGieRnYFYz_hQVVOlFUkgrKMnjL3Mrer4aCIIpArGYKbOKu8VUBhYkAgsi9ogbZRxyvgpYWF396zxzlHs2tV-IZVqk9Fxul2328-U5YOKTEfhqxIV1OkSbwBEjxDhjJvZOHbg',
    'x-careem-operating-system': 'iOS/18.6.1',
    'accept-language': 'en',
    'x-careem-permissions': 'location:granted',
    'lat': '25.254298691412355',
    'x-careem-appengine-api-version': '2025-07-07',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

params = {
    'query': 'burger',
}

response = requests.get(
    'https://appengine.careemapis.com/v1/page/food-hybrid-dishes-search',
    params=params,
    cookies=cookies,
    headers=headers,
)