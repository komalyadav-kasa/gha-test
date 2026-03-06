from flask import Flask, jsonify, request

app = Flask(__name__)


def validate_name(name):
    if not isinstance(name, str):
        raise TypeError(f"Expected a string, got {type(name).__name__}")
    return name.strip()


@app.route("/hello", methods=["POST"])
def hello_world():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Request must be JSON"}), 400

    name = body.get("name")
    if name is None:
        return jsonify({"error": "Missing required field: name"}), 400

    try:
        validated = validate_name(name)
    except TypeError as e:
        return jsonify({"error": str(e)}), 400

    if not validated:
        return jsonify({"error": "name must not be blank"}), 400

    return jsonify({"message": f"Hello, {validated}!"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
