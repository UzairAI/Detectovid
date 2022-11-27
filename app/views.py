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

model = load_model('app/detectovid.h5')
model.make_predict_function()

def getMelSpectogram(input_path, output_path, show=False):
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

    img = utils.load_img(output_path, target_size=(150, 150))
    img_tensor = utils.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor
 
@app.route('/', methods=['GET','POST'])
def home():
    return render_template("index.html", color1 = '#ffffff', color = 'red')
 

# Route triggered whn the upload is successful
@app.route('/result', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        f = request.files['audio']
        snd_loc = os.path.join(app.root_path, "static/img","audio.wav")
        img_loc = os.path.join(app.root_path, "static/img","audio.png")
        f.save(snd_loc)
        if (os.path.getsize(snd_loc) > 0) and (os.path.exists(snd_loc)):

            img = getMelSpectogram(snd_loc, img_loc)
            
            output = model.predict(img)

            os.remove(snd_loc)
            os.remove(img_loc)
            covid = "{0:.2f}".format(output[0][0]*100)
            healthy = "{0:.2f}".format(output[0][1]*100)
            result = f'Covid : {covid}% Healthy : {healthy}%'
            if float(covid) > 50:
                color1 = 'red'
                color = 'red'
            elif float(healthy) >= 50:
                color1 = '#8bc34a'
                color = '#8bc34a'
            else:
                color1 = '#ffffff'
                color = 'red'

            return render_template("index.html", prediction_text = result, color = color, color1 = color1)
        else:
            return redirect(url_for('home'))