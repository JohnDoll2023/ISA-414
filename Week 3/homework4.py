def ip2address(ips):    
    import requests
    import pandas

    df = pandas.DataFrame()

    for ip in ips:
        url = "https://api.ipgeolocation.io/ipgeo?apiKey=addfff7fcd22470aa78fd9a66cbdf500&ip=" + ip
        response = requests.get(url).json()
        response_df = pandas.DataFrame.from_dict(response, orient='index').transpose()
        
        if df.empty:
            df = response_df
        else:
            df = df.append(response_df)
    
    df.index = pandas.RangeIndex(len(df.index))
    
    return df


ip_addresses= ["165.70.141.165", "93.215.167.191", "197.177.61.197", "206.236.177.182","5.77.63.24", "158.227.31.151", "82.233.65.66", "63.123.244.194"]

web_data = ip2address(ip_addresses)
web_data = web_data[["ip", "country_name", "city", "latitude", "longitude"]]
web_data.to_csv("web_data.csv", index=False)