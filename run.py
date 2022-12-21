# Run the Flask app for debugging or development.
import os

from src.project.app import create_app

app_env = os.environ['APP_ENV']
app = create_app(app_env)

if __name__ == "__main__":
    ssl_context = None
    if app.config["ENABLE_ADHOC_SSL"]:
        ssl_context = ("/etc/apps/pki/ssl/server.crt", "/etc/apps/pki/ssl/server.key")
    app.run(host="0.0.0.0", threaded=True, ssl_context=ssl_context)
