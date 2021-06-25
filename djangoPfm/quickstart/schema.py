import re
import string
from nltk.tokenize import word_tokenize
import graphene
import nltk
from nltk.stem import WordNetLemmatizer
from graphene_django import DjangoObjectType
from nltk.corpus import stopwords
from rest_framework.utils import json
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from .models import News

class NewsType(DjangoObjectType):
    class Meta:
        model = News
        fields = ['id','url', 'title', 'content','datePost','language','classe']


class Query(graphene.ObjectType):
     all_news = graphene.List(NewsType)

     # --- Resolvers --- #
     def resolve_all_news(root, info):
         return News.objects.all()


#create & update
class CreateNews(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
        title=graphene.String()
        content=graphene.String()
    news=graphene.Field(NewsType)
    @classmethod
    def mutate(self,info,new_data=None):
        news=News(
            title=new_data.title,
            content=new_data.content
        )
        news.save()
        return CreateNews(news=news)


# --- Class for Mutations --- #
class Mutations(graphene.ObjectType):
     CreateNews.Field()
# -------------------------- NLP Services -------------------------- #
# --- Tokenization --- #
class Tokenization(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    text = info.context.get('txt')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    word_tokens = nltk.word_tokenize(text)
    return {"result":word_tokens}

def tokenize(text):
  schema_ = graphene.Schema(Tokenization)
  result = schema_.execute('{ txt }', context={'txt': text})
  data = result.data['txt'].replace("\'", "\"")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res

# --- Stop Words --- #
class StopWords(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    stop_words = set(stopwords.words('arabic'))
    text = info.context.get('txt')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    word_tokens = nltk.word_tokenize(text)
    without_stop_words = [w for w in word_tokens if not w in stop_words]
    return {"result":without_stop_words}

def stopword(text):
  schema = graphene.Schema(StopWords)
  result = schema.execute('{ txt }', context={'txt': text})
  data = result.data['txt'].replace("\'", "\"")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res

# --- Lemmatization --- #
class Lemmatization(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    text = info.context.get('txt') #.encode('utf8')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    lemmatized = []
    for word in word_tokens:
      lemmatized.append(nltk.ISRIStemmer().suf32(word))
    return {"result":lemmatized}

def lemmatize(text):
  schema = graphene.Schema(Lemmatization)
  result = schema.execute('{ txt }', context={'txt': text})
  data = result.data['txt'].replace("\'", "\"")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res

# --- Stemming --- #
class Stemming(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    text = info.context.get('txt') #.encode('utf8')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    stemmer = PorterStemmer()
    word_tokens = word_tokenize(text)
    stemmed = []
    for word in word_tokens:
      stemmed.append(stemmer.stem(word))
    return {"result":stemmed}

def stem(text):
  schema = graphene.Schema(Stemming)
  result = schema.execute('{ txt }', context={'txt': text})
  data = result.data['txt'].replace("\'", "\"")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res

# --- Pos Tagging --- #
class PosTagging(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    stop_words = set(stopwords.words('arabic'))
    text = info.context.get('txt')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    word_tokens = nltk.sent_tokenize(text)
    for i in word_tokens:
      word_list = nltk.word_tokenize(i)
      word_list = [word for word in word_list if not word in stop_words]
      tagged = nltk.pos_tag(word_list)
      return {"result":tagged}

def postag(text):
  schema = graphene.Schema(PosTagging)
  result = schema.execute('{ txt }', context={'txt': text})
  da = result.data['txt'].replace("\'", "\"")
  dat = da.replace("(", "[")
  data = dat.replace(")", "]")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res

# --- Bag of words --- #
class BagOfWords(graphene.ObjectType):
  txt = graphene.String()
  def resolve_txt(root, info):
    text = info.context.get('txt')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    txt = [text]
    vect = CountVectorizer()
    vect.fit(txt)
    to_array = vect.transform(txt).toarray()
    bag_of_words = to_array.tolist()
    return {"result":bag_of_words}

def bagofwords(text):
  schema = graphene.Schema(BagOfWords)
  result = schema.execute('{ txt }', context={'txt': text})
  data = result.data['txt'].replace("\'", "\"")
  res = json.dumps(json.loads(data)["result"], ensure_ascii=False).encode('utf8')
  res = res.decode()
  res = res.replace("\"", "")
  res = res.replace("[", "")
  res = res.replace("]", "")
  return res




schema = graphene.Schema(query=Query)#,mutation=Mutations