from base.models import Topic

def topics(request):
    # Retrieve all topics or customize based on your logic
    all_topics = Topic.objects.all()
    
    # Make the topics available in every template
    return {'all_topics': all_topics}