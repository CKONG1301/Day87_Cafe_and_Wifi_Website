from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField, URLField
from wtforms.validators import DataRequired, InputRequired, URL
import csv
from datetime import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

coffee_rating = [(0, '✘'), (1, '☕'), (2, '☕☕'), (3, '☕☕☕'), (4, '☕☕☕☕'), (5,'☕☕☕☕☕')]
wifi_rating = [(0, '✘'), (1,'💪'), (2,'💪💪'), (3, '💪💪💪'), (4, '💪💪💪💪'), (5,'💪💪💪💪💪')]
power_rating = [(0, '✘'), (1,'🔌'), (2,'🔌🔌'), (3, '🔌🔌🔌'), (4, '🔌🔌🔌🔌'), (5,'🔌🔌🔌🔌🔌')]

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[InputRequired(), URL()])
    open = TimeField('Opening Time e.g. 8AM', validators=[InputRequired()])
    close = TimeField('CLosing Time e.g. 5:30PM', validators=[InputRequired()])
    coffee = SelectField('Cafe Rating', validators=[InputRequired()], choices=coffee_rating, validate_choice=False)
    wifi = SelectField('Wifi Strength Rating', validators=[InputRequired()], choices=wifi_rating)
    power = SelectField('Power', validators=[InputRequired()], choices=power_rating)
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline="", encoding="utf8") as csv_file:
            location_url = form.location.data
            open_time = form.open.data.strftime("%I:%M%p")
            close_time = form.close.data.strftime("%I:%M%p")
            coffee_rate = coffee_rating[int(form.coffee.data)][1]
            wifi_rate = wifi_rating[int(form.wifi.data)][1]
            power_rate = power_rating[int(form.power.data)][1]
            print(f"{coffee_rate},{wifi_rate}, {power_rate}")
            csv_file.write(f"{form.cafe.data},{location_url},{open_time},{close_time},{coffee_rate},{wifi_rate},{power_rate}\n")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
