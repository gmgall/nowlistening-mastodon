from pprint import pprint
from mastodon import Mastodon
import pylast
import os

LAST_API_KEY = os.environ['LAST_API_KEY']

MAST_ACC_TOKEN = os.environ['MAST_ACC_TOKEN']
INSTANCE_URL = os.environ['INSTANCE_URL']


def now_listening_str():
    network = pylast.LastFMNetwork(api_key=LAST_API_KEY)
    user = pylast.User(os.environ['LAST_USER'], network)
    now_playing = user.get_now_playing()
    if not now_playing: return None
    track_name = now_playing.get_title()
    artist_name = now_playing.get_artist().get_name()
    return track_name + ' - ' + artist_name

def update_fields():
    mastodon = Mastodon(access_token=MAST_ACC_TOKEN, api_base_url=INSTANCE_URL)
    profile_fields = mastodon.account_verify_credentials()['source']['fields']
    has_now_listening_field = False
    for row in profile_fields:
        del row['verified_at']
        if row['name'] == 'Ouvindo agora 🔊':
            has_now_listening_field = True
            row['value'] = now_listening_str()

    if not has_now_listening_field:
        profile_fields.append({ 'name': 'Ouvindo agora 🔊', 'value': now_listening_str()})
    new_profile_fields = [row for row in profile_fields if row['value'] is not None]
    new_profile_tuples = [tuple(row.values()) for row in new_profile_fields]
    result = mastodon.account_update_credentials(fields = new_profile_tuples)

    return result

print(now_listening_str())
pprint(update_fields())
