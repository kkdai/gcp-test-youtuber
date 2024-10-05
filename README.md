# YouTube Data Loader

This project is a Flask application designed to load YouTube data using the Google API. It is optimized for deployment on Google Cloud Run and leverages Google Cloud's Secret Manager for secure management of API credentials. The application uses the `langchain_community` library to interact with YouTube data.

## Features

- Fetches YouTube data using channel names or video IDs.
- Securely manages API credentials with Google Cloud Secret Manager.
- Provides a RESTful API endpoint to load YouTube data.
- Designed for seamless deployment on Google Cloud Run.

## Prerequisites

- Python 3.7 or higher
- Google Cloud account with Secret Manager API enabled
- YouTube API credentials stored in Google Cloud Secret Manager
- Flask
- `langchain_community` library

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kkdai/gcp-test-youtuber.git
   cd gcp-test-youtuber
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**

   Ensure the following environment variables are set:

   - `PROJECT_ID`: Your Google Cloud project ID.
   - `PORT`: The port on which the Flask app will run (default is 8080).

4. **Store YouTube API credentials in Google Cloud Secret Manager:**

   - Create a secret named `youtube_api_credentials` in your Google Cloud project.
   - Store your YouTube API credentials JSON in this secret.

## Deploying to Google Cloud Run

1. **Build and deploy the application:**

   Use the Google Cloud SDK to build and deploy the application to Cloud Run:

   ```bash
   gcloud builds submit --tag gcr.io/$PROJECT_ID/youtube-data-loader
   gcloud run deploy youtube-data-loader --image gcr.io/$PROJECT_ID/youtube-data-loader --platform managed
   ```

2. **Access the application:**

   - Once deployed, you will receive a URL for your Cloud Run service.
   - Visit the URL to access the application endpoints:
     - `/` for the "Hello, World!" message.
     - `/load-youtube-data` to load YouTube data.

## Logging

The application uses Python's built-in logging module to log debug information. Logs include details about secret fetching, temporary file creation, and data loading processes.

## Error Handling

If an error occurs during the data loading process, the application will log the error and return a JSON response with the error message.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
