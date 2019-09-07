

from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)
api_url_users = 'https://zenden-api-heroku.herokuapp.com/api/Users'
api_url_houses = 'https://zenden-api-heroku.herokuapp.com/api/Houses/'
api_url_matches = 'https://zenden-api-heroku.herokuapp.com/api/Matches'


@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/users/",  methods=["GET", "POST"])
def users(): 
    res = request.args.to_dict()
    
    # allow optional fields to be None
    age = res['age'] if 'age' in res and res['age'].strip() else None
    income = res['income'] if 'income' in res and res['income'].strip() else None
    address = res['address'] if 'address' in res and res['address'].strip() else None

    create_row_data = {
            "education": res['education'],
            "gender": res['gender'],
            "city": res['city'],
            "address": address,
            "income": income,
            "age": age,
            "state": res['state'],
            "name": res['name'],
            "email": res['email'],
            "zipcode": res['zipcode'],
            "sjsu_affiliated": bool(res['sjsu_affiliated']), 
            "ownership": res["ownership"], 
            "housing_method": res["housing"]
        }
    r = requests.post(url=api_url_users, json=create_row_data)
    print(r.status_code, r.reason, r.text)
    r_json = r.json()
    user_id = r_json["data"]['user_id']
    print(user_id)
    return redirect(url_for('houses', user_id = user_id))

@app.route("/houses/")
def houses():
    if 'user_id' not in request.args: 
        return render_template("signup.html")
    user_id = request.args['user_id'] 
    complete_url = api_url_houses + '1?user_id=' + user_id
    r = requests.get(url=complete_url)
    r_json = r.json()
    first_photo = r_json["data"][0]["urls"].split(' ')[0]
    house_id = r_json["data"][0]["house_id"]
    address = r_json["data"][0]["address"]
    city = r_json["data"][0]["city"]
    state = r_json["data"][0]["state"]
    num_bedrooms = r_json["data"][0]["num_bedrooms"]
    num_bathrooms = r_json["data"][0]["num_bathrooms"]
    house_sqft = r_json["data"][0]["house_sqft"]
    print(r.status_code, r.reason, r.text)
    return render_template('houses.html', 
            data=first_photo, 
            user_id=user_id, 
            house_id=house_id, 
            address=address, 
            city=city,
            state=state, 
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms, 
            house_sqft=house_sqft
            )

@app.route("/results/",  methods=["GET", "POST"])
def results(): 
    res = request.args.to_dict()
    print(res)
    if 'button1' in res.keys(): 
        result_list = res['button1'].split(',')
        user_id = result_list[1]
        house_id = result_list[2]
        create_row_data = {
            "house_id": house_id, 
            "user_id": user_id, 
            "predicted_score": -1, 
            "actual_score": 0, 
            "viewed": True
        }
        r = requests.post(url=api_url_matches, json=create_row_data)
        print('No')
    elif 'button2' in res.keys(): 
        result_list = res['button2'].split(',')
        user_id = result_list[1]
        house_id = result_list[2]
        create_row_data = {
            "house_id": house_id, 
            "user_id": user_id, 
            "predicted_score": -1, 
            "actual_score": 1, 
            "viewed": True
        }
        r = requests.post(url=api_url_matches, json=create_row_data)
        print('Yes')
    else: 
        pass
    return redirect(url_for('houses', user_id = user_id))

if __name__ == '__main__': 
    app.run(port=8000, debug=True)






