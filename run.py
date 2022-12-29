# Run the Flask app for debugging or development.
import os

from src.project.app import create_app

app_env = os.getenv('APP_ENV', 'local')
app = create_app(app_env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
