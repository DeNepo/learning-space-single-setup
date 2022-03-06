import os
import sys
import json
import yaml
import requests

PROJECTS_BASE_URL = 'https://api.github.com/projects'
REPOS_BASE_URL = 'https://api.github.com/repos'

# both TOKEN and REPOSITORY are expected to be passed in during the action run
TOKEN = os.environ['TOKEN']
# this variable has the format "user/project" from https://github.com/user/project
REPOSITORY = os.environ['REPOSITORY']

# it's not ideal to do this all in one big function, but unfortunately, the way that
# the GitHub API expects the call to create cards from issues, we need both the column ID
# and the issue ID, and that's easier to do inside the same scope
def main():
    yaml_path = os.environ['INPUT_PATH']

    with open(yaml_path, 'r') as input_file:
        data = yaml.safe_load(input_file)

    board_data = data['board']

    print('creating project board')
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {TOKEN}'
    }
    body = {
        'name': board_data['name'],
        'body': board_data['description']
    }

    response = requests.post(
        f'{REPOS_BASE_URL}/{REPOSITORY}/projects',
        json=body,
        headers=headers
        )

    # we need this project ID of the newly created project board to create the columns
    project_id = response.json()['id']
    
    for column_name in board_data['columns']:
        response = requests.post(
            f'{PROJECTS_BASE_URL}/{project_id}/columns',
            data=json.dumps({'name': f'{column_name}'}),
            headers=headers
            )
        if column_name == 'TODO':
            # because column IDs aren't predictable, we need to grab this one explicitly to reference later
            column_id = response.json()['id']

    # we're done creating the base board, now we add some issues to be added as cards in the TODO column
    materials_data = data['materials']

    print('creating issues')

    for material in materials_data:
       response = requests.post(
           f'{REPOS_BASE_URL}/{REPOSITORY}/issues',
           data=json.dumps({'title': material['name'], 'body': material['description'] + f"\n{material['url']}"}),
           headers=headers
           )

       issue_id = response.json()['id']

       # create some cards on the TODO column
       response = requests.post(
           f'{PROJECTS_BASE_URL}/columns/{column_id}/cards',
           data=json.dumps({'content_id': issue_id, 'content_type': 'Issue'}),
           headers=headers
           )

    print('all done!')

if __name__ == "__main__":
    main()
