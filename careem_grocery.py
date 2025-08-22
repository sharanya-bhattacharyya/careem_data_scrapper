import requests

cookies = {
    '_cfuvid': 'KUfKE7ask8nHxZH9rfmY9aTsyLkGGSL99V3MgCSNGjo-1755799517036-0.0.1.1-604800000',
    'dtCookiez48j3ehh': 'v_4_srv_6_sn_6F0F4F28A151B784ABA0905D94AEA2E8_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1',
    '__cf_bm': 'L4KPYDRceaDU5rtRVU6dydn4rSuREkogZOnZpkWNRRE-1755799299-1.0.1.1-aS_jPgXKmR4VcZgz14knZ1YPOS12w13fi9kIDeoF3eYYixxEedyew24FgbGRuLk4tdpOPSNirZK__wIYAcEnfknj1iX07p0Krl2px_jtpQ8',
}

headers = {
    'x-careem-agent': 'ICMA',
    'session_id': '47D505A9-3149-41CA-B1B1-31A19A0AB41F',
    'x-careem-beta': 'false',
    # 'cookie': '_cfuvid=KUfKE7ask8nHxZH9rfmY9aTsyLkGGSL99V3MgCSNGjo-1755799517036-0.0.1.1-604800000; dtCookiez48j3ehh=v_4_srv_6_sn_6F0F4F28A151B784ABA0905D94AEA2E8_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; __cf_bm=L4KPYDRceaDU5rtRVU6dydn4rSuREkogZOnZpkWNRRE-1755799299-1.0.1.1-aS_jPgXKmR4VcZgz14knZ1YPOS12w13fi9kIDeoF3eYYixxEedyew24FgbGRuLk4tdpOPSNirZK__wIYAcEnfknj1iX07p0Krl2px_jtpQ8',
    'user-agent': 'ICMA/25.32.0',
    'x-careem-session-id': '47D505A9-3149-41CA-B1B1-31A19A0AB41F',
    'agent': 'ICMA',
    'time-zone': 'Asia/Dubai',
    'lng': '55.29878167051707',
    'x-careem-appengine-page-session-id': '1dc0f04d-cd8b-498f-94e5-b0e2827365ff',
    'version': '25.32.0',
    'x-careem-version': '25.32.0',
    'x-careem-user-location': '25.25424948347514,55.29878167051707',
    'x-careem-appengine-api-version': '2025-07-07',
    'authorization': 'Bearer eyJraWQiOiJlYTU4Y2VlZS0yMmU2LTRhNzEtYjkzOS0xNWE3N2IzNzQ3MGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3ODMwNjYyMSIsImF1ZCI6ImNvbS5jYXJlZW0uaW50ZXJuYWwiLCJhY2Nlc3NfdHlwZSI6IkNVU1RPTUVSIiwidXNlcl9pZCI6NzgzMDY2MjEsImF6cCI6IjI4MWYwY2JhLWI1MGMtNDZjZC04ZGUwLWUzNTVkZWMwODk3Yi5pY21hLmNhcmVlbS5jb20iLCJraW5kIjoiQ1VTVE9NRVIiLCJzY29wZSI6IndlYmxvZ2luX2F1dGhlbnRpY2F0b3IgcGF5X3dhbGxldF9jaGFuZ2VfY3VycmVuY3kgc3Vic2NyaXB0aW9ucyB3YWxsZXQgYWRkcmVzcyBvcGVuaWQgeGNtYSBwcm9maWxlIHBheW1lbnRzIG90cCBjbGllbnRfbWFuYWdlbWVudCBkZWxpdmVyaWVzIGNwYXlfYW9zX3JlYWQgY3BheV93YWxsZXRfY3VzdG9tZXIgcGhvbmUgb2ZmbGluZV9hY2Nlc3MgbG9jYXRpb25zIGJvb2tpbmdzIGVtYWlsIiwiaXNzIjoiaHR0cHM6XC9cL2lkZW50aXR5LmNhcmVlbS5jb21cLyIsImV4cCI6MTc1NTg1MzkxOCwiaWF0IjoxNzU1NzY3NTE4LCJqdGkiOiJiMjdmMjYzOC04MzViLTRiZjQtYmU2Yi1lNjJjNWQ0NDBhNWEifQ.jQTGBDNzG5EhUCmRYm3spiMTAks6cJCz-ZdmlHNP1CvZRTuqlnNtdY0ax0glsOszgew8F4D_ldHDKKfnpU6Kp2IZXw8qzWav3xXrDJd2RBKYEgNpmP3WQuKgvNHr1Zjw0MnmUKMZevdnRRyvzMa7yZtnY89-6gvTOOSIG_MZw_wUsaaG8DownriqoA8iTHEMQtdvZYdB7_Q8reFE3nRan7PRqGWKl3XOARESkqeppzff3JRYY9y71JSsri8sUos02ox0WkLq9nQrQGZ7VFaTD4LncFtXCO4xcHkKdGjp84dUBHZGqBke13k9cLNV-FNbbGsJHIp5NFBrQZcRoFctFg',
    'x-careem-operating-system': 'iOS/18.6.1',
    'x-careem-permissions': 'location:granted',
    'accept-language': 'en',
    'lat': '25.25424948347514',
    'x-careem-device-id': 'D0Do1cW3V2mftjsX',
    'accept': '*/*',
}

params = {
    'selectedServiceAreaId': '0',
    'refreshCounter': '5',
}

response = requests.get(
    'https://appengine.careemapis.com/v1/page/ea-discovery-home',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.status_code)
print(response.text[:500])  # Print the first 500 characters of the response for brev
print(response.headers)
print(response.json())  # Print the JSON response if available