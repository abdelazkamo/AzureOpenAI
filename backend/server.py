from blueprints_registration import register_blueprints
from config import Config
from quart import Quart, jsonify
from quart_cors import cors

app = Quart(__name__)

app.config.from_object(Config)

# CORS Config
app = cors(app, allow_origin="*", expose_headers=["X-Page-Number", "page_number"])


register_blueprints(app=app)


@app.route("/flask-api/")
async def index():
    return jsonify({"message": "Server is Up and Running!"}), 200


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        import logging

        logging.exception("Error starting the server: %s", e)
