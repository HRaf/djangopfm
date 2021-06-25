from django.apps import AppConfig

from djangoPfm.quickstart.training import TrainingModels
import pickle
import json, codecs
from json import JSONEncoder

class QuickstartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoPfm.quickstart'





'''@djangoPfm.quickstart.route("/fakenews/<text>", methods=['get'])
def fakenews(text):
  model = pickle.load(open('model.sav', 'rb'))
  prediction = TrainingModels.predict(model, text)
  prediction = prediction.tolist()
  prediction = json.dumps(prediction)
  prediction = prediction.replace("[", "")
  prediction = prediction.replace("]", "")
  return {'result': prediction}'''
