from idlelib.sidebar import temp_enable_text_widget

from flask import (
    Blueprint, render_template
)

bp = Blueprint("landing", __name__)

@bp.route('/')
def index():
    temperature = 25
    humidity = 15
    return render_template('index.html', temperature=temperature, humidity=humidity)