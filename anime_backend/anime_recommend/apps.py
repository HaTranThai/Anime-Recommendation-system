from django.apps import AppConfig

class AnimeRecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime_recommend'

    def ready(self):
        import anime_recommend.signals 