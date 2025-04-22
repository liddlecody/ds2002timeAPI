from flask import Flask, jsonify, request
from datetime import datetime
from zoneinfo import ZoneInfo
from functools import wraps

app = Flask(__name__)

API_TOKEN = "supersecrettoken123"

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized – provide a valid Bearer token"}), 401

    return decorator

CAPITAL_TIMEZONES = {
    "washington": "America/New_York",        # USA (Washington, D.C.)
    "london": "Europe/London",              # United Kingdom
    "paris": "Europe/Paris",                # France
    "berlin": "Europe/Berlin",              # Germany
    "moscow": "Europe/Moscow",              # Russia
    "beijing": "Asia/Shanghai",             # China (Beijing)
    "new delhi": "Asia/Kolkata",            # India (New Delhi)
    "tokyo": "Asia/Tokyo",                  # Japan
    "canberra": "Australia/Sydney",         # Australia
    "ottawa": "America/Toronto",            # Canada
}


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

@app.route("/api/capital-time/<string:capital>", methods=["GET"])
@token_required
def capital_time(capital: str):
    """Return local time & UTC offset for the given capital city."""
    tz_name = CAPITAL_TIMEZONES.get(capital.lower())
    if not tz_name:
        return (
            jsonify(
                {
                    "error": f"Capital '{capital}' not found in database.",
                    "available_capitals": sorted(CAPITAL_TIMEZONES.keys()),
                }
            ),
            404,
        )

    now = datetime.now(ZoneInfo(tz_name))
    offset_raw = now.strftime("%z") 
    offset_formatted = f"{offset_raw[:3]}:{offset_raw[3:]}" if offset_raw else None

    return jsonify(
        {
            "capital": capital.title(),
            "local_time": now.isoformat(timespec="seconds"),
            "utc_offset": offset_formatted,
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)






