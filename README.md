Telegram Message
===

## Instructions

1. create telegrem app at http://my.telegram.org/

    - login with telephone
    - click "API development tools" to create new application with
      - App title
      - Short name
      - Platform: "Other"
    - get "App api_id" and "App api_hash"

2. fill config
3. run script

python fetch_members.py
python send_message.py members.csv
python add_to_group.py members.csv

## TODO

1. async version