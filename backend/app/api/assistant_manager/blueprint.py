from app.database.db_operation import DB_Operations
from quart import Blueprint, current_app, jsonify, request
from .assistant_process import AssistantProcess

assistant_blueprint = Blueprint("assistant", __name__)


@assistant_blueprint.route("/generate", methods=["POST"])
async def generate():
    json_data = await request.json
    assistant_process = AssistantProcess(app_config=current_app.config)
    response = await assistant_process.generate_response(
        user_query=json_data["user_query"],
    )

    # Return the first result as JSON
    return jsonify(response), 200
