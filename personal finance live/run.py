from dotenv import load_dotenv
from app import create_app


# Load environment variables from .env file
load_dotenv()

# create app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
