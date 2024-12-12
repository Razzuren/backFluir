import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is required. Check your environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", google_api_key=gemini_api_key)
app = Flask(__name__)
CORS(app)


@app.route("/complete", methods=["POST"])
def generate_completion():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            app.logger.warning("Prompt is missing in the request.")
            return jsonify({"error": "Prompt is required."}), 400

        response = llm.invoke("Complete o seguinte texto, sem formatações: " + prompt)
        app.logger.info(f"LLM Response: {response.content}")

        return jsonify({"completion": response.content})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/referral", methods=["POST"])
def process_referral():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            app.logger.warning("Input text is missing in the request.")
            return jsonify({"error": "Input text is required."}), 400

        referral_response = llm.invoke("Gere um JSON seguindo o seguinte padrão: "
                                       "{\"espe\": \"value\","
                                       "\"diag\": \"value\","
                                       "\"compl\": \"value\"}"
                                       "onde espe é a especialidade, diag é o diagnóstico e compl é a queixa principal,"
                                       "baseado no texto: " + text)

        app.logger.info(f"Referral Response: {referral_response.content}")

        return jsonify({"result": referral_response})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

# @app.route("/referal", methods=["POST"])
# def process_referral():
#     try:
#         data = request.get_json()
#         text = data.get("text", "").strip()
#
#         if not text:
#             app.logger.warning("Input text is missing in the request.")
#             return jsonify({"error": "Input text is required."}), 400
#
#         referral_response = llm.invoke("Gere um JSON seguindo o seguinte padrão: "
#                                        "{\"espe\": \"value\","
#                                        "\"diag\": \"value\","
#                                        "\"compl\": \"value\"}"
#                                        "onde espe é a especialidade, diag é o diagnóstico e compl é a queixa principal,"
#                                        "baseado no texto: " + text)
#
#         app.logger.info(f"Referral Response: {referral_response.content}")
#
#         return jsonify({"result": referral_response})
#     except Exception as e:
#         app.logger.error(f"Error occurred: {str(e)}")
#         return jsonify({"error": str(e)}), 500
#
# this is the endpoint
# the model might return som unwanted stuff, can we filter to get only the json content and return it?
#
