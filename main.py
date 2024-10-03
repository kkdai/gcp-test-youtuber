import os
import json
from flask import Flask, jsonify
from google.cloud import secretmanager
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

app = Flask(__name__)


def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['PROJECT_ID']}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def init_google_api_client():
    creds_content = json.loads(get_secret("youtube_api_credentials"))
    credentials = Credentials.from_authorized_user_info(creds_content)
    return build("youtube", "v3", credentials=credentials)


@app.route("/load-youtube-data", methods=["GET"])
def load_youtube_data():
    try:
        youtube = init_google_api_client()

        # Use a Channel
        channel_response = (
            youtube.channels()
            .list(part="snippet,contentDetails,statistics", forUsername="Reducible")
            .execute()
        )

        # Use Youtube Ids
        video_response = (
            youtube.videos()
            .list(part="snippet,contentDetails,statistics", id="TrdevFK_am4")
            .execute()
        )

        return jsonify({"channel_data": channel_response, "video_data": video_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
