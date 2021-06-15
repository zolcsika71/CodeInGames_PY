import json

from user_data import game_id

# read the replay from file
with open(f'{game_id}.json', 'r') as f:
    replay = json.loads(f.read())

stderr = []

for frame in replay['frames']:
    if 'stderr' not in frame.keys():
        continue
    for err in frame['stderr'].split('\n'):
        # some of my stderr lines aren't referee input. I marked them with '#' to filter them
        if not err.startswith('#'):
            stderr.append(err)

# write the error stream to the file 'input.txt'
with open('input.txt', 'w+') as f:
    f.write('\n'.join(stderr))
print('\n'.join(stderr))
