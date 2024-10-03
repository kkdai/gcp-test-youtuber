import os
from flask import Flask, jsonify
from google.cloud import secretmanager
from langchain_community.document_loaders import GoogleApiClient, GoogleApiYoutubeLoader

app = Flask(__name__)


def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['PROJECT_ID']}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def init_google_api_client():
    creds_content = get_secret("youtube_api_credentials")
    return GoogleApiClient(credentials_json=creds_content)


@app.route("/load-youtube-data", methods=["GET"])
def load_youtube_data():
    try:
        google_api_client = init_google_api_client()

        # Use a Channel
        youtube_loader_channel = GoogleApiYoutubeLoader(
            google_api_client=google_api_client,
            channel_name="Reducible",
            captions_language="en",
        )

        # Use Youtube Ids
        youtube_loader_ids = GoogleApiYoutubeLoader(
            google_api_client=google_api_client,
            video_ids=["TrdevFK_am4"],
            add_video_info=True,
        )

        # Load data
        channel_data = youtube_loader_channel.load()
        ids_data = youtube_loader_ids.load()

        return jsonify({"channel_data": str(channel_data), "ids_data": str(ids_data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
