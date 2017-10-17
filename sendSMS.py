import urllib
import urllib2
import json

#send the message

def send(api_key, api_secret, PhoneNumber, msg):
    params = {
        'api_key': api_key,
        'api_secret': api_secret,
        'to': PhoneNumber,#'972547807312', #PhoneNumber,#'972504204785', #PhoneNumber
        'from': 'MTnexmo',
        'text': msg,#'Hello from Nexmo' #msg
    }

    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)

    request = urllib2.Request(url)
    request.add_header('Accept', 'application/json')
    response = urllib2.urlopen(request)

    # check if the massage was sent
    if response.code == 200:
        data = response.read()
        # Decode JSON response from UTF-8
        decoded_response = json.loads(data.decode('utf-8'))
        # Check if your messages are succesful
        messages = decoded_response["messages"]
        for message in messages:
            if message["status"] == "0":
                print "success"
                return 1
    else:
        # Check the errors
        print "unexpected http {code} response from nexmo api".response.code
    return 0
