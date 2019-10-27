from app import app


@app.route('/')
def index():
    return "Blog Home."