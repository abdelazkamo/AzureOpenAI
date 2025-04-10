from app.database.db_operation import DB_Operations
from quart import Blueprint, current_app, jsonify, request

assistant_blueprint = Blueprint("assistant", __name__)


@assistant_blueprint.route("/generate", methods=["POST"])
async def generate():
    db = DB_Operations()
    await db.init_db()

    # Get the query parameter

    # Fetch data from the database
    sql_query = "SELECT * FROM Users"
    result = await db.execute_query(query=sql_query, should_fetch_data=True)

    if not result:
        return jsonify({"message": "No results found"}), 404

    # Return the first result as JSON
    return jsonify(result[0]), 200
