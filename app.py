import pyrebase

config = {
	"apiKey": "AIzaSyAND8NR1JNgFv8qDQIg0weG-WMpd3S5r_U",
    "authDomain": "ee16b-speed-tracker.firebaseapp.com",
    "databaseURL": "https://ee16b-speed-tracker.firebaseio.com",
    "projectId": "ee16b-speed-tracker",
    "storageBucket": "ee16b-speed-tracker.appspot.com",
    "messagingSenderId": "17172022833",
    "appId": "1:17172022833:web:b5f1390da31811f4e8b710",
    "measurementId": "G-N57WJXHNF6"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

from flask import * 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def basic_1():
	today_lecture = db.child("lecture").get()
	if today_lecture.val() != None:
		all_items = list(today_lecture.val().values())
		print(all_items)
		slower = len([val for val in all_items if val == "Slower"])
		right = len([val for val in all_items if val == "Just right"])
		faster = len([val for val in all_items if val == "Faster"])
	else:
		slower = 0
		right = 0
		faster = 0
		to_be_displayed = "No Lecture Selected Yet"
	return render_template('index.html', slower=slower, right=right, faster=faster, 
                            max=max([slower, right, faster]),
                            labels=['Slower', 'Just right', 'Faster'],
                            values=[slower, right, faster])


@app.route('/', methods=['POST'])
def basic_2():
	today_lecture = db.child("lecture").get()
	if request.method == 'POST':
		option = request.form.getlist('options')
		choice = option[0]
		db.child("lecture").push(choice)
		if db.child("lecture").get().val() != None:
			all_items = list(db.child("lecture").get().val().values())
			slower = len([val for val in all_items if val == "Slower"])
			right = len([val for val in all_items if val == "Just right"])
			faster = len([val for val in all_items if val == "Faster"])
		else:
			slower = 0
			right = 0
			faster = 0
		return render_template('index.html',slower=slower, right=right, faster=faster, 
			max=max([slower, right, faster]),
							labels=['Slower', 'Just right', 'Faster'],
							values=[slower, right, faster])
	return render_template('index.html')



if __name__ == '__main__':
	app.run(debug=True)