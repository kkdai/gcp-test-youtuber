import os
import json
import tempfile
from google.cloud import secretmanager
from langchain_community.document_loaders import GoogleApiClient, GoogleApiYoutubeLoader


def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['PROJECT_ID']}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def create_temp_credentials_file():
    creds_content = get_secret('youtube_api_credentials')
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        json.dump(json.loads(creds_content), temp_file)
    return temp_file.name


def init_google_api_client():
    creds_path = create_temp_credentials_file()
    return GoogleApiClient(credentials_path=creds_path)


def load_youtube_data():
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
        add_video_info=True
    )

    # Load data
    channel_data = youtube_loader_channel.load()
    ids_data = youtube_loader_ids.load()

    return channel_data, ids_data


if __name__ == "__main__":
    channel_data, ids_data = load_youtube_data()
    print("Channel Data:", channel_data)
    print("IDs Data:", ids_data)
