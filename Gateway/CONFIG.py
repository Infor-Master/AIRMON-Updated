url = "https://airmon.ufp.pt/api/parse"
#url = "http://192.168.43.46:4000/api/parse"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
publicKeyCert = "cert/public.pem"

networks = [
    ['WPA2', 'test', '13572469'],
    ['WPA2E', 'eduroam', '012938', 'convidado@ufp'],
    #['WPA2E', 'eduroam', 'ola123', 'teste@ufp.pt'],
    #['WPA2E', 'eduroam', '250595559', '36824@ufp.pt']
    #['WPA2', 'ZON-5100', 'ba876d3a1a72'],
    #['WPA2', 'Vodafone-69E89E', 'bx6ByA2G6V']
    ]
