from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
WEBEX_TEAMS_ACCESS_TOKEN="NDQyM2MzNGEtN2QxYS00Mzc4LWI3NWEtN2U4YWEafaefaeNTZhNmZkZTAtZmU3"

flask_app = Flask(__name__)
api = WebexTeamsAPI(access_token=WEBEX_TEAMS_ACCESS_TOKEN)

# Your Webex Teams webhook should point to http://<serverip>:5000/events
@flask_app.route('/events', methods=['GET', 'POST'])
def webex_teams_webhook_events():
    if request.method == 'POST':
        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        # Create a Webhook object from the JSON data
        webhook_obj = Webhook(json_data)
        room = api.rooms.get(webhook_obj.data.roomId)
        message = api.messages.get(webhook_obj.data.id)
        person = api.people.get(message.personId)

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        me = api.people.me()
        if message.personId == me.id:
            return 'Bot message'
        else:
            msg = api.messages.create(roomId=room.id, text="Sample text")
            return 'Answer sent'

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=9900)
