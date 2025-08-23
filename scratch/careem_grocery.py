import requests

cookies = {
    '_cfuvid': 'U7BB98yk5bmHOdmMnnn4qzOskWVjgjLr0NcbhQQ8xl4-1755968988869-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_4_sn_179CEEA3D2F0B156337696B73F4F8F9A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    '__cf_bm': 'MqYljBwQHn3UX6DyotZlivzrraNIr1v7BiINuMRt.Dk-1755968980-1.0.1.1-MtAsAn5Zzxrp2ujP89VCDrhUAS1i1r9RxsB0s5GtVjIT7EpJqMg1UG0Wsfk98YurmSah2QakM.4cZx8D34.WL_EtIlviFrFpl0q4RjkAp2E',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
    'x-careem-beta': 'false',
    # 'cookie': '_cfuvid=U7BB98yk5bmHOdmMnnn4qzOskWVjgjLr0NcbhQQ8xl4-1755968988869-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_4_sn_179CEEA3D2F0B156337696B73F4F8F9A_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; __cf_bm=MqYljBwQHn3UX6DyotZlivzrraNIr1v7BiINuMRt.Dk-1755968980-1.0.1.1-MtAsAn5Zzxrp2ujP89VCDrhUAS1i1r9RxsB0s5GtVjIT7EpJqMg1UG0Wsfk98YurmSah2QakM.4cZx8D34.WL_EtIlviFrFpl0q4RjkAp2E',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': 'A0413A6A-62DD-457D-A721-CE25DDB8EA95',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '55.298776468959815',
    'x-careem-appengine-page-session-id': 'af9cc31c-cf7f-4a43-b4af-850e705e92e5',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.25427759908695,55.298776468959815',
    'x-careem-appengine-api-version': '2025-07-07',
    'authorization': 'Bearer eyJraWQiOiIzOGU2OTcxMS03MjFiLTQxMTctYmUxNi02Y2Y0ZjkzOTAyZWMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NjA1MzAyMywiaWF0IjoxNzU1OTY2NjIzLCJqdGkiOiI5ZGI1OWJjZi1lYTg2LTRiMTEtYjBkZi1jOWY4MWZkNjBjYjAifQ.YZY61hclPjNGXjFtYnv2vaW905gfKLJIv0UYEy4ajDfm5h-HOP0jsQWKkWxYl9P3FnBkYSAsjk5AbaGoS-dWNiXiYeCrb1JrnFK0xUikCiob1p3YcxevvSp6teLYAkSPHqeazP0yruT1lrup0bnsqCwvqCoYNaOj8VZsbVrBxyaLg2cggvJqyWzqlm90q_bR-DK_zc0XhJfpyMB_K-O9bo7hH-OPyxJ7J9Gq9IPmkZjJNy1xMIAuTdU7CQP1UkL2PXFYEAfybsstqFDOOSqXDWAa7m87CKdz5M__TIA1sgRbKzFbVncuAnVQbukRoL6SRu7zfBl6bnE7olozePFptA',
    'x-careem-operating-system': 'iOS/18.6.1',
    'x-careem-permissions': 'location:granted',
    'accept-language': 'en',
    'lat': '25.25427759908695',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

params = {
    'brand_id': '1012099',
}

response = requests.get(
    'https://appengine.careemapis.com/v1/page/quik-discovery-home',
    params=params,
    cookies=cookies,
    headers=headers,
)