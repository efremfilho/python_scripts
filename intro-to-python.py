import requests
import json

exemplo = 10000.51 #var exemplo = 10000.51;

print(exemplo) #Logger.log('o valor de exemplo é '+ exemplo)

exemplo = 'efrem'

exemplo = exemplo + 5 #diferente do GS

exemplo = 'efrem_'

#Exemplo de condicional - https://www.w3schools.com/python/python_conditions.asp

if exemplo == 'efrem':
    exemplo = exemplo + " maranhão"
elif exemplo == 'efrem_':
    exemplo = exemplo + ' filho'
else:
    exemplo = exemplo + "-"
    if isinstance(exemplo, basestring):
        exemplo = exemplo + " maranhão filho"

"""
if(exemplo == 'efrem'){
  exemplo = exemplo + ' maranhao';
} else {
  exemplo = exemplo + "-";

if(parseInt(exemplo,10)) {
    exemplo = exemplo + ' silva';
  }
}
"""

# Exemplo de loop - https://www.w3schools.com/python/python_for_loops.asp
efrems = ["efrem", "efrem_", "efrem+"]
for x in efrems:
  print(x)

for i in range(10,1000,6): 
    j = float(i)
    print(j/10)

"""
  for (var i = 1; i < 100; i = i + .6) {
    if (Math.floor(i) == Math.round(i)) {
      //Logger.log('o round é ' + Math.round(i) + ' e eu contei '+ i);
    } else {
      //Logger.log('o round é ' + Math.round(i) + ' e eu não contei o decimal' + i);
    }
  }
"""

# Exemplo API Externa - https://medium.com/quick-code/absolute-beginners-guide-to-slaying-apis-using-python-7b380dc82236 
# Para o Google Maps API - https://console.developers.google.com/apis/credentials?project=universidade-agora
request = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-7.136722,-34.845641&radius=20000&types=restaurant&key=AIzaSyCG828zfyvYvUx-FmMx6R_JRNLcH_9uvo0')
data = request.json()

for place in data['results']:
    print(place['vicinity'])
    
"""request = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-7.136722,-34.845641&radius=20000&types=restaurant&key=AIzaSyCG828zfyvYvUx-FmMx6R_JRNLcH_9uvo0')
data = request.json()

print(data)

for place in data:
    print(place)
request = requests.get('http://api.open-notify.org')
print(request.text)
"""

"""
  var url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-7.136722,-34.845641&radius=20000&types=restaurant&key=[YOUR-KEY]';
  var response = UrlFetchApp.fetch(url);
  var json = response.getContentText();
  var data = JSON.parse(json);
  
  //Logger.log(data.results.length);
  
  for(var a = 0; a<data.results.length; a++){
    //Logger.log(data.results[0].vicinity);
    Logger.log('O lugar se chama: '+data.results[a].name + 
    ' \ne tem coordenadas (latitude,longitude) em: '+ 
    data.results[a].geometry.location.lat+','+data.results[a].geometry.location.lng);
  }
"""

#parsed = json.loads(data)
print(json.dumps(data, indent=4, sort_keys=True))
