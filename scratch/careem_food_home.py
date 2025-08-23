import requests

cookies = {
    '_cfuvid': 'xMWRgNv.Q7Hqi0dwbNyXDTadlU.pZ_wWPdVI6Yp_u5Q-1755968052094-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_4_sn_50CC5D85F82345BA404FA486851C035A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    '__cf_bm': 'QOQt1JGSRcyZKty7apjQPNLX1eSoowuzuwUn2bPpchM-1755968015-1.0.1.1-vwjkE0WC0qYeMMt6YHcGrD73iNZfx_ibTODMfI.RTT82jxzx1deBoM7gov6MYkgiFUaZqiy0yMyAScAbZE2PUGfSKxCVZi660NDbFac7hRw',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
    'x-careem-beta': 'false',
    # 'cookie': '_cfuvid=xMWRgNv.Q7Hqi0dwbNyXDTadlU.pZ_wWPdVI6Yp_u5Q-1755968052094-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_4_sn_50CC5D85F82345BA404FA486851C035A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; __cf_bm=QOQt1JGSRcyZKty7apjQPNLX1eSoowuzuwUn2bPpchM-1755968015-1.0.1.1-vwjkE0WC0qYeMMt6YHcGrD73iNZfx_ibTODMfI.RTT82jxzx1deBoM7gov6MYkgiFUaZqiy0yMyAScAbZE2PUGfSKxCVZi660NDbFac7hRw',
    'x-careem-delivery-location': '25.25429965142188,55.29878644330265',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': '21C7750A-962F-4DDC-B62E-3DA1C8CA828F',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '55.29878644330265',
    'x-careem-appengine-page-session-id': 'dc00ad78-5509-492c-975f-3d4cc6c24945',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.25429965142188,55.29878644330265',
    'x-careem-appengine-api-version': '2025-07-07',
    'x-careem-operating-system': 'iOS/18.6.1',
    'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA',
    'x-careem-permissions': 'location:granted',
    'accept-language': 'en',
    'lat': '25.25429965142188',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

response = requests.get('https://appengine.careemapis.com/v1/page/food-discovery-home', cookies=cookies, headers=headers)