from django.shortcuts import render
import plotly.express as px
from glidermap.models import GliderMeasurement
import pandas as pd
from django.http import JsonResponse

def glider_map_view(request):
    return render(request, 'glider_map.html')
def plot_glider_data(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Missing coordinates'}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    tolerance = 0.01
    qs = GliderMeasurement.objects.filter(
        latitude__range=(lat - tolerance, lat + tolerance),
        longitude__range=(lon - tolerance, lon + tolerance)
    ).values('timestamp', 'depth', 'temperature', 'salinity', 'oxygen', 'cdom')

    df = pd.DataFrame(list(qs))

    if df.empty:
        return JsonResponse({'plot_html': "<p style='color:red;'>No data found to plot.</p>"})

    fig = px.scatter(
        df,
        x="timestamp",
        y="depth (m)",
        color="temperature (°C)",
        size="salinity",
        hover_data=["oxygen", "cdom"],
        title="Glider Profile: Depth vs Time",
    )
    fig.update_layout(width=700, height=700)
    return JsonResponse({'plot_html': fig.to_html(full_html=False)})
def glider_locations(request):
    glider_loc= list(GliderMeasurement.objects.values('latitude','longitude').distinct())
    return JsonResponse(glider_loc, safe=False)    
    