import json
import requests
import sys

from user_data import email, pw, userID, game_id

# the session object saves cookies
with requests.Session() as s:
    # let's login first
    p = s.post('https://www.codingame.com/services/CodingamerRemoteService/loginSiteV2', json=[email, pw, True])
    # the same request as above, but with a session object
    r = s.post('https://www.codingame.com/services/gameResultRemoteService/findByGameId', json=[str(game_id), userID])
    replay = r.json()
with open(f'{game_id}.json', 'w+') as f:
    f.write(json.dumps(replay))

# read the replay from file
with open(f'{game_id}.json', 'r') as f:
    replay = json.loads(f.read())

stderr = []

for idx in range(len(replay['frames'])):
    frame = replay['frames'][idx]
    if 'stderr' not in frame.keys():
        continue
    for err in frame['stderr'].split('\n'):
        # some of my stderr lines aren't referee input. I marked them with '#' to filter them
        if not err.startswith('#'):
            stderr.append(err)

# write the error stream to the file 'input.txt'
with open('input.txt', 'w+') as f:
    f.write('\n'.join(stderr))
# print('\n'.join(stderr))
