from .headers import *

# PRevents the application from caching the inputs to the browser
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def getMelSpectogram(input_path, output_path):
    sound = input_path
    y, sr = librosa.load(sound, mono=True, duration=3)
    librosa.feature.melspectrogram(y=y, sr=sr)
    D = np.abs(librosa.stft(y))**2
    S = librosa.feature.melspectrogram(S=D, sr=sr)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    plt.savefig(output_path)
 
@app.route('/', methods=['GET','POST'])
def home():
    return render_template("Detectovid.html")
 

# Route triggered whn the upload is successful
@app.route('/result', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['audio']
        getMelSpectogram(f, os.path.join(app.root_path, "static/img","audio.png"))
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

        with open(app.root_path + "/static/img/audio.png", "rb") as image_contents:
            results = predictor.classify_image(
                projectId, publish_iteration_name, image_contents.read())
            result=""
            for prediction in results.predictions:
                result += "\t\t\n" + prediction.tag_name + " : {0:.2f}% ".format(prediction.probability * 100)

        return render_template("Detectovid.html", prediction_text = result)  




