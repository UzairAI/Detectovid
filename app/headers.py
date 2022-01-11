from flask import *
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from app import app



prediction_key = "8681749f7f654adcbe07120e07e8cd62"
publish_iteration_name = "DetectovidPredict"
ENDPOINT = "https://detectcovid-prediction.cognitiveservices.azure.com/"
projectId = "c92a7818-cc01-490c-8bc9-997da165c4e9"

