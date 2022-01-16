# Detectovid
This web app can detect if a person has covid-19 with 73% accuracy.

The app is developed using Azure Web APP, Azure Custom Vision and Azure Active Directory.
Dataset used is the Coswara Dataset by IISc and only the heavy-cough sounds are used.

It takes .wav sound files as input and converts them to a Mel-Spectogram and saves it as a .png image.
The then generated image is sent to Azure Custom Vision Model which predicts whether a person has covid or not.

Some sample files from the dataset are added to the TestData directory which can be used to test the application.
It does not take into consideration empty or non-cough sound files.

Dataset source- https://arxiv.org/abs/2005.10548
