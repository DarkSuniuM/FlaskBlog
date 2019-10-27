from . import admin


@admin.route('/')
def index():
    return "Hello from admin Index"
