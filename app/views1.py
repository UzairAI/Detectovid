from .functions import getMelSpectogram
from .headers import *

@app.after_request
def add_header(r):

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template("Detectovid.html")

@app.route("/", methods=["GET", "POST"])
def success():
    if request.method == 'POST':  
        f = request.files['file']
        f = getMelSpectogram(f, os.path.join(app.root_path, "static","audio.png"))
        #f.save(os.path.join(app.root_path, "static","audio.png")) 

        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

        with open(app.root_path + "/static/audio.png", "rb") as image_contents:
            results = predictor.classify_image(
                projectId, publish_iteration_name, image_contents.read())
            result=""
            for prediction in results.predictions:
                result += "\t\t\n" + prediction.tag_name + " : {0:.2f}% ".format(prediction.probability * 100)

        return render_template("Detectovid.html", prediction_text = result)

        #if file:
	    #target = f'/static/img/{file.filename[:-3].replace(".", "")}.png'
            #fn.getMelSpectogram(file, )
            #with audioFile as source:
            #    data = recognizer.record(source)
            #transcript = recognizer.recognize_google(data, key=None)



if __name__ == "__main__":
    app.run(debug=True, threaded=True)