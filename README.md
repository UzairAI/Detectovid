# Detectovid
This web app can detect if a person has covid-19 with 73% accuracy.

The app is developed using Azure Web APP, Azure Custom Vision and Azure Active Directory.
Dataset used is the Coswara Dataset by IISc and only the heavy-cough sounds are used.

It takes .wav sound files as input and converts them to a Mel-Spectogram and saves it as a .png image.

**The following python script converts the .wav sound file to mel-spectogram and stores as .png:**

```

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
    
```

# Azure Services Used:

1. **Azure Custom Vision:** The Mel spectograms are sent as an intput to Azure Custom Vision Model, which predicts the result and displays on the web app.
![image](https://user-images.githubusercontent.com/69196090/149898222-09e87988-3c06-43e3-83d3-0aa190991990.png)



2. **Azure Web App:** The flask app is deployed using azure web app and can be accesses via https://detectovid.azurewebsites.net
![image](https://user-images.githubusercontent.com/69196090/149898478-b34f8a57-c22a-48bd-afe6-bebc8b2c71f1.png)



3. **Azure Active Directory:** The app is made secure using Azure Active Directory which is used for Authenticating the user.

**Note :** Restrict access is currently set to allow unauthorized access for project evaluation.
![image](https://user-images.githubusercontent.com/69196090/149901463-2fb6534c-d47f-4807-8498-43b2b6a41838.png)



# Test Data
The app can be either tested using custom or personal sound or using the test data available at:
**https://github.com/UzairAI/Detectovid/tree/master/TestData**

**Note:** It does not take into consideration empty or non-cough sound files.

**Dataset source:** https://arxiv.org/abs/2005.10548

# Screenshots:

![image](https://user-images.githubusercontent.com/69196090/149897186-83ab2f86-62e9-4a6e-9146-c16075b747c8.png)
![image](https://user-images.githubusercontent.com/69196090/149897512-9566bf34-3534-4619-90ce-03eb0fb3856e.png)

