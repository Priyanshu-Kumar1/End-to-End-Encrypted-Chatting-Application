import requests
import json

# OneSignal app ID and REST API key
app_id = "f4a48b57-05da-478f-99af-fed3e8ae98ac"
api_key = "MjBhNmI3MmMtMDRiMi00YWQ5LThlNWMtMWYwNjBkOTZhNGJk"

# Function to set player tags
def set_player_tags(player_id, tags):
    data = {
        "app_id": app_id,
        "player_id": player_id,
        "tags": tags
    }
    response = requests.put(
        "https://onesignal.com/api/v1/players/" + player_id,
        headers={"Content-Type": "application/json; charset=utf-8",
                 "Authorization": "Basic " + api_key},
        data=json.dumps(data)
    )
    print(response.content)

set_player_tags("")
