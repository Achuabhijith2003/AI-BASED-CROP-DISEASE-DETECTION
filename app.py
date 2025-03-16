from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def dashboard():
    try:
        return render_template('template\dashboard.html')
    except Exception as e:
        app.logger.error(f"Error rendering template: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)