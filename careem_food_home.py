import requests

cookies = {
    '__cf_bm': 'CFnGH8nkwi.8tbp82kSiyO2cRYnWjhkOhYbWgq0Yobc-1755797459-1.0.1.1-yd0Zv0JmxaBmX6UWCebZB2rXrUH0hWDi.jtAMkrunSE_iWqMd4B2k0b_lxUTD6WxIB29nSjwQ0t4t1yeh9eUnT7TBrSJPPKgbziB5BGutAo',
    '_cfuvid': 'fuRqjaJrqXU_0E4jUd7CA6DbwW3B3wZBUyxzKjUtJIg-1755797459320-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_2_sn_E3F12AC21924F6E68EFEE2E0BCAE1AEF_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': 'FDF2AC92-9E9F-4183-B78A-03D2E293DF21',
    'x-careem-beta': 'false',
    # 'cookie': '__cf_bm=CFnGH8nkwi.8tbp82kSiyO2cRYnWjhkOhYbWgq0Yobc-1755797459-1.0.1.1-yd0Zv0JmxaBmX6UWCebZB2rXrUH0hWDi.jtAMkrunSE_iWqMd4B2k0b_lxUTD6WxIB29nSjwQ0t4t1yeh9eUnT7TBrSJPPKgbziB5BGutAo; _cfuvid=fuRqjaJrqXU_0E4jUd7CA6DbwW3B3wZBUyxzKjUtJIg-1755797459320-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_2_sn_E3F12AC21924F6E68EFEE2E0BCAE1AEF_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': 'FDF2AC92-9E9F-4183-B78A-03D2E293DF21',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '55.298781716044736',
    'x-careem-appengine-page-session-id': 'dc27b859-50f6-42d6-94a9-08f03541fb60',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.25424952005592,55.298781716044736',
    'x-careem-appengine-api-version': '2025-07-07',
    'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTg1MzkxOCwiaWF0IjoxNzU1NzY3NTE4LCJqdGkiOiJiMjdmMjYzOC04MzViLTRiZjQtYmU2Yi1lNjJjNWQ0NDBhNWEifQ.jQTGBDNzG5EhUCmRYm3spiMTAks6cJCz-ZdmlHNP1CvZRTuqlnNtdY0ax0glsOszgew8F4D_ldHDKKfnpU6Kp2IZXw8qzWav3xXrDJd2RBKYEgNpmP3WQuKgvNHr1Zjw0MnmUKMZevdnRRyvzMa7yZtnY89-6gvTOOSIG_MZw_wUsaaG8DownriqoA8iTHEMQtdvZYdB7_Q8reFE3nRan7PRqGWKl3XOARESkqeppzff3JRYY9y71JSsri8sUos02ox0WkLq9nQrQGZ7VFaTD4LncFtXCO4xcHkKdGjp84dUBHZGqBke13k9cLNV-FNbbGsJHIp5NFBrQZcRoFctFg',
    'x-careem-operating-system': 'iOS/18.6.1',
    'x-careem-permissions': 'location:granted',
    'accept-language': 'en',
    'lat': '25.25424952005592',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

params = {
    'selectedServiceAreaId': '0',
    'refreshCounter': '4',
}

response = requests.get(
    'https://appengine.careemapis.com/v1/page/ea-discovery-home',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.status_code)
print(response.text[:500])  # Print the first 500 characters of the response for brevity
print(response.headers)
print(response.json())  # Print the JSON response if available