from dotenv import load_dotenv
import os 
import base64

from requests import post, get
import json

load_dotenv() # load env file

client_id = os.getenv("CLIENT_ID") # Get value of env var
client_secret = os.getenv("CLIENT_SECRET")

def get_token(): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8") #encode auth string into bytes
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") # encodes string in base 64 & convert back to utf-8

    url = "https://accounts.spotify.com/api/token" 
    headers = {     # dictionary with headers + encoded authentication string
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"} # data to be sent in POST request
    result = post(url, headers = headers, data = data) # Send post request to url with headers and data
    json_result = json.loads(result.content) # parse json response content into python
    token = json_result["access_token"] # Extract access token from json response
    return token 

def get_auth_header(token): # Take oAuth token & return dictionary with authorization
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" # Spotify search endpoint (action)
    headers = get_auth_header(token) # get auth headers
    query = f"?q={artist_name}&type=artist&limit=1" #construct search query with artists name

    query_url = url + query # Concatenate url
    result = get(query_url, headers= headers) # send GET req to query URL
    json_result = json.loads(result.content)["artists"]["items"] # Parse responds content & extracts specifics
    if len(json_result) == 0:
        print("That artist does not exist!")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, "Weezer")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

# loop thru printing top songs
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")