from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import send_file

app = Flask(__name__)

'''
@app.route('/plot/')
def plot():
    try:
        # try to get the query string like ?width=xxx&height=xxx
        height = int(request.args.get('height'))
        width = int(request.args.get('width'))
    except ValueError:
        # if height, width not available, set a default value
        height, width = 100, 100
    # I randomly generate the plot which just based on H x W
    # you should be able to generate yours from your library
    to_draw = np.random.randint(0, 255, (height, width))
    img = plt.imshow(to_draw)
    # you can convert the graph to arrays and save to memory
    imgIO = StringIO()
    img.write_png(imgIO, noscale=True) # save to memory
    imgIO.seek(0)
    # and send that image as file as static file of url
    # like... /plot/?width=100&height=100
    return send_file(imgIO, mimetype='image/png')

# this is the main page with the form and user input
@app.route('/', methods=['GET', 'POST'])
def index():
    # set the default values
    height, width = 100, 100
    # handle whenever user make a form POST (click the Plot button)
    if request.method == 'POST':
        try:
            # use this to get the values of user input from the form
            height = int(request.form['height'])
            width = int(request.form['width'])
        except ValueError:
            pass
    # and pass the context back to the template
    # if no form is POST, default values will be sent to template        
    return render_template('blabla.html', height=height, width=width)



'''
@app.route("/")
def index():
	return render_template('index.html')

@app.route('/queryresult/', methods=['POST'])
def queryresult():
    query=request.form['searchquery']
    return render_template('queryresult.html', query = query)


#searchapi
@app.route("/viewresult")
def view():
	return render_template('viewresult.html')

if __name__ == "__main__":
    app.run(debug = True)
