import os
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

app = Flask(__name__)


# Initialize Gemini
genai.configure(api_key="AIzaSyBOs7lQsFcwlYn61XNZtaqv1OgXk0g7aww")

# Create the model and chat globally
model = genai.GenerativeModel(model_name="gemini-pro")
chat = model.start_chat()

# Set initial context for the mental health assistant
initial_prompt = """You are a compassionate mental health assistant called Raji specifically designed to help people in rural India dealing with depression and mental health challenges. Your role is to:

1. Provide culturally sensitive support and guidance
2. Use simple, clear language that's easy to understand
3. Be aware of the limited mental health resources in rural areas
4. Incorporate local cultural context and values in your responses
5. Suggest practical coping strategies that are feasible in rural settings
6. Recognize when to recommend seeking professional help
7. Be empathetic and non-judgmental in all interactions
8. Respect local customs and beliefs while providing scientific advice
9. Address stigma around mental health in rural communities
10. Provide information about available local mental health resources when possible
11.Give short responses only please

Remember to maintain a supportive and understanding tone throughout the conversation."""

# Initialize the chat with the context
chat.send_message(initial_prompt)

# Set the SQLite database file to the /tmp directory (Vercel's writable directory)
db_path = os.path.join('/tmp', 'responses.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model for storing responses
class QuestionnaireResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Q1 = db.Column(db.Integer)
    Q2 = db.Column(db.Integer)
    Q3 = db.Column(db.Integer)
    Q4 = db.Column(db.Integer)
    Q5 = db.Column(db.Integer)
    Q6 = db.Column(db.Integer)
    Q7 = db.Column(db.Integer)
    Q8 = db.Column(db.Integer)
    Q9 = db.Column(db.Integer)
    Q10 = db.Column(db.Integer)
    Q11 = db.Column(db.Integer)
    Q12 = db.Column(db.Integer)
    Q13 = db.Column(db.Integer)
    Q14 = db.Column(db.Integer)
    Q15 = db.Column(db.Integer)
    Q16 = db.Column(db.Integer)
    Q17 = db.Column(db.Integer)
    Q18 = db.Column(db.Integer)
    Q19 = db.Column(db.Integer)
    Q20 = db.Column(db.Integer)
    Q21 = db.Column(db.Integer)
    Q22 = db.Column(db.Integer)
    Q23 = db.Column(db.Integer)
    Q24 = db.Column(db.Integer)
    Q25 = db.Column(db.Integer)
    Q26 = db.Column(db.Integer)
    Q27 = db.Column(db.Integer)
    Q28 = db.Column(db.Integer)
    Q29 = db.Column(db.Integer)
    Q30 = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract data from the form and save to the database
        response = QuestionnaireResponse(
            Q1=int(request.form.get('Q1', 0)),
            Q2=int(request.form.get('Q2', 0)),
            Q3=int(request.form.get('Q3', 0)),
            Q4=int(request.form.get('Q4', 0)),
            Q5=int(request.form.get('Q5', 0)),
            Q6=int(request.form.get('Q6', 0)),
            Q7=int(request.form.get('Q7', 0)),
            Q8=int(request.form.get('Q8', 0)),
            Q9=int(request.form.get('Q9', 0)),
            Q10=int(request.form.get('Q10', 0)),
            Q11=int(request.form.get('Q11', 0)),
            Q12=int(request.form.get('Q12', 0)),
            Q13=int(request.form.get('Q13', 0)),
            Q14=int(request.form.get('Q14', 0)),
            Q15=int(request.form.get('Q15', 0)),
            Q16=int(request.form.get('Q16', 0)),
            Q17=int(request.form.get('Q17', 0)),
            Q18=int(request.form.get('Q18', 0)),
            Q19=int(request.form.get('Q19', 0)),
            Q20=int(request.form.get('Q20', 0)),
            Q21=int(request.form.get('Q21', 0)),
            Q22=int(request.form.get('Q22', 0)),
            Q23=int(request.form.get('Q23', 0)),
            Q24=int(request.form.get('Q24', 0)),
            Q25=int(request.form.get('Q25', 0)),
            Q26=int(request.form.get('Q26', 0)),
            Q27=int(request.form.get('Q27', 0)),
            Q28=int(request.form.get('Q28', 0)),
            Q29=int(request.form.get('Q29', 0)),
            Q30=int(request.form.get('Q30', 0))
        )
        db.session.add(response)
        db.session.commit()

        # Calculate the total score
        total_score = sum([
            response.Q1, response.Q2, response.Q3, response.Q4, response.Q5,
            response.Q6, response.Q7, response.Q8, response.Q9, response.Q10,
            response.Q11, response.Q12, response.Q13, response.Q14, response.Q15,
            response.Q16, response.Q17, response.Q18, response.Q19, response.Q20,
            response.Q21, response.Q22, response.Q23, response.Q24, response.Q25,
            response.Q26, response.Q27, response.Q28, response.Q29, response.Q30
        ])
        return redirect(url_for('result', response_id=response.id))

    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat_endpoint():  # Renamed from 'chat' to avoid conflict
    try:
        user_input = request.json.get('user_input')
        print(f"Received user input: {user_input}")

        if not user_input:
            return jsonify({"error": "No user input provided!"}), 400

        try:
            response = chat.send_message(user_input)
            model_response = response.text
            print(f"Model response: {model_response}")

            return jsonify({"response": model_response})

        except Exception as model_error:
            print(f"Model error: {str(model_error)}")
            return jsonify({"error": f"Model error: {str(model_error)}"}), 500

    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/result/<int:response_id>")
def result(response_id):
    # Fetch the response from the database
    response = QuestionnaireResponse.query.get_or_404(response_id)

    # Calculate the total scores for each group
    q1_to_q10_sum = sum([response.Q1, response.Q2, response.Q3, response.Q4, response.Q5,
                         response.Q6, response.Q7, response.Q8, response.Q9, response.Q10])

    q11_to_q20_sum = sum([response.Q11, response.Q12, response.Q13, response.Q14, response.Q15,
                          response.Q16, response.Q17, response.Q18, response.Q19, response.Q20])

    q21_to_q30_sum = sum([response.Q21, response.Q22, response.Q23, response.Q24, response.Q25,
                          response.Q26, response.Q27, response.Q28, response.Q29, response.Q30])

    # Determine the type of depression
    depression_type = None
    if q1_to_q10_sum > 20:
        depression_type = "Major Depression"
    elif q11_to_q20_sum > 20:
        depression_type = "Bipolar Depression"
    elif q21_to_q30_sum > 20:
        depression_type = "Sad Depression"
    else:
        depression_type = "No significant signs of depression"

    return render_template("result.html", total_score=q1_to_q10_sum + q11_to_q20_sum + q21_to_q30_sum,
                           depression_type=depression_type)


if __name__ == "__main__":
    app.run(debug=True,port=5001)