from django.urls import path
from .views import glider_map_view, plot_glider_data,glider_locations

urlpatterns = [
     path('', glider_map_view, name='glider_map'),
     path('plot-glider-data/', plot_glider_data, name='plot_glider_data'),
     path('gliderdata/',glider_locations)
]