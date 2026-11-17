from flask import Flask, request, jsonify
from zeep import Client
from zeep.exceptions import Fault

app = Flask(__name__)

WSDL_URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"


def validate_country_code(value):
    if not isinstance(value, str):
        raise ValueError("Country code must be a string.")

    code = value.strip().upper()

    if len(code) != 2 or not code.isalpha() or not code.isascii():
        raise ValueError(
            "Country code must contain exactly two letters, such as NG or US."
        )

    return code


def get_country_info(value):
    code = validate_country_code(value)

    try:
        client = Client(WSDL_URL)

        name = client.service.CountryName(sCountryISOCode=code)

        if not name or name.strip().lower() == "country not found":
            raise ValueError(f"No country found for code '{code}'.")

        capital = client.service.CapitalCity(sCountryISOCode=code)
        currency = client.service.CountryCurrency(sCountryISOCode=code)

        return {
            "status": "success",
            "country_code": code,
            "country": name,
            "capital": capital,
            "currency_code": currency.sISOCode,
            "currency_name": currency.sName,
        }

    except ValueError:
        raise
    except Fault as exc:
        raise RuntimeError(f"SOAP service error: {exc}")
    except Exception as exc:
        raise RuntimeError(f"Unable to communicate with SOAP service: {exc}")


@app.route("/country", methods=["GET"])
def country_get():
    try:
        result = get_country_info(request.args.get("code"))
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"status": "error", "message": f"Invalid input: {exc}"}), 400
    except RuntimeError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 502


@app.route("/country", methods=["POST"])
def country_post():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return (
            jsonify(
                {"status": "error", "message": "Please provide a valid JSON object."}
            ),
            400,
        )

    try:
        result = get_country_info(data.get("code"))
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"status": "error", "message": f"Invalid input: {exc}"}), 400
    except RuntimeError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 502


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "application": "SOAP Country Information API",
            "description": "Retrieves country information from a public SOAP service",
            "GET": "/country?code=NG",
            "POST": "/country",
            "example_country_codes": ["NG", "US", "GB", "CA"],
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
