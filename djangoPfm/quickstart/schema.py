import graphene
from graphene_django import DjangoObjectType
from .models import News

class NewsType(DjangoObjectType):
    class Meta:
        model = News
        fields = ['id', 'title', 'content']


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





schema = graphene.Schema(query=Query)#,mutation=Mutations