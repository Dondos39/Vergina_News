from  .models import Article



def imp_news(request):
    rum = Article().__class__.objects.get_important()
    return dict(rum=rum)





    
