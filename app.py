from flask import Flask, render_template, request, redirect
import final_proj
import requests
import model


global valid_restaurant_params,valid_weather_params
valid_restaurant_params=['list','ratings','price','top','bottom','category','map']
valid_weather_params=['weather']


app = Flask(__name__)

@app.route('/')
def search_restaurant():
    return render_template('search.html', entries=model.get_entries())


@app.route("/add")
def addentry():
    ## add a guestbook entry
    return render_template("addentry.html")

@app.route("/postentry", methods=["POST"])
def postentry():
    name = request.form["name"]
    message = request.form["message"]
    model.add_entry(name, message)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def postdelete():
    id = request.form['id']
    model.delete_entry(int(id))
    return redirect('/')

@app.route("/modify", methods=["POST"])
def postmodify():
    id = request.form['id']
    text=request.form['new_message']
    model.modify_entry(int(id),text)
    return redirect('/')




@app.route('/r',methods=['POST'])
def update_database():
    global response,weather,category,res_li
    try:
        location = request.form['location']
        number = request.form['number']
        category = request.form['category']
        response = location.lower()
        response_li = response.split(',')
        response = response_li[0].strip()+', '+response_li[1].strip()
        category = category.strip().lower()
        final_proj.get_city_restaurant(location= str(response), type= str(category),number=number)
        final_proj.get_city_weather(response_li[0].strip())
        final_proj.init_db()
        final_proj.insert_db()
        res_li = final_proj.get_full_info(city= str(response),category= str(category),number= number)
        weather = final_proj.weather_city(response)
        return redirect('/rs')
    except:
        return redirect('/')


@app.route('/rs',methods=['GET','POST'])
def restaurant_search_result():
    global res_li
    weather_condition = weather[0][1]
    temp = '%.2f' %(weather[0][2]-273.15)
    wind = weather[0][3]
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        res_li = final_proj.get_all_res_info(sortby, sortorder)
    else:
        res_li= final_proj.get_all_res_info()
    return render_template("restaurant_display.html", city=response.upper(),weather_condition=weather_condition,
    temp=temp, wind=wind, res_list=res_li)


@app.route('/rs/plot',methods=['GET','POST'])
def plot_option():
    final_proj.restaurant_location_query(response,category)
    html = final_proj.plot_restaurant_site_offline(response)
    return html

@app.route('/details',methods=['GET','POST'])
def details():
    global res_li
    category =[]
    search_dict = {}
    for i in res_li:
        category.append(i[5]+' food introduction')
    for j in category:
        search_dict[j]=final_proj.wikipedia.search(j)
    return render_template("details.html", search_dict = search_dict)

@app.route('/details2',methods=['GET','POST'])
def details2():
    food_type = request.form['detail']
    detail = final_proj.get_details_food('food')
    return render_template("details2.html", detail = detail)

if __name__ == '__main__':
    final_proj.init_db()
    model.init()
    app.run(debug=True)
