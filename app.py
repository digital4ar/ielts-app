import os
from flask import Flask, render_template, request, session
from openai_api import generate_study_plan
from language_data import translations

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required to enable session tracking

# Bonus resources
def get_bonus_links():
    return {
        "StarterKit": "https://www.sparkskytech.com/free-resources",
        "HubPreviewPDF": "https://www.sparkskytech.com/product/ielts-mastery-hub-preview",  # PDF/MP4 preview
        "HubShop": "https://www.sparkskytech.com/shop/learning-education/ielts-mastery-hub"
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    lang = request.form.get('lang', 'en')
    t = translations.get(lang, translations['en'])  # fallback to English
    study_plan = None
    message = None
    bonus_links = get_bonus_links()

    # Initialize session plan counter
    if 'plan_count' not in session:
        session['plan_count'] = 0

    # Handle form submission
    if request.method == 'POST' and 'level' in request.form:
        if session['plan_count'] >= 2:
            message = (
                "🚫 You’ve reached your free limit. Upgrade to unlock more study plans."
                if lang == 'en'
                else "🚫 لقد وصلت إلى الحد المجاني. قم بالترقية للوصول إلى خطط إضافية."
            )
        else:
            # Collect user inputs
            level = request.form['level']
            target = request.form['target']
            test_type = request.form['test_type']
            test_mode = request.form['test_mode']

            # Build prompt for OpenAI
            prompt = f"""
            Create a personalized 4-week IELTS study plan for a student with:
            - English level: {level}
            - Target band score: {target}
            - Test type: {test_type}
            - Test mode: {test_mode}

            Provide the plan in {'Arabic' if lang == 'ar' else 'English'}.
            Use ALL CAPS and headings like "======= WEEK 1 =======" or "================ الأسبوع الأول ================" to separate each week.
            Include weekly tasks for Listening, Reading, Writing, and Speaking.
            Highlight differences based on {test_type} format and adjust for {test_mode}.
            Keep tone friendly, clear, and practical.
            """

            study_plan = generate_study_plan(prompt)
            session['plan_count'] += 1

    return render_template(
        'home.html',
        t=t,
        lang=lang,
        study_plan=study_plan,
        bonus_links=bonus_links,
        message=message
    )

# Port configuration for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
