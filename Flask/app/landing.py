from flask import (
    Blueprint, render_template
)
from app.data_storage import data_store

# definition of a blueprint object
bp = Blueprint("landing", __name__)

# defining the route on which the blueprint should be rendered
@bp.route('/')
def index():
    data = data_store.get()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    return render_template('index.html', temperature=temperature, humidity=humidity)