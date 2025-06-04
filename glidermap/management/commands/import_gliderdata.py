from django.core.management.base import BaseCommand
from glidermap.models import GliderMeasurement
import xarray as xr
import pandas as pd

class Command(BaseCommand):
    help = 'Imports NetCDF glider data into the database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['filepath']
        self.stdout.write(f"Reading file: {file_path}")
        
        ds = xr.open_dataset(file_path)

        df = pd.DataFrame({
            "timestamp": pd.to_datetime(ds['precise_time'].values).tz_localize("UTC"),
            "latitude": ds['latitude'].values,
            "longitude": ds['longitude'].values,
            "depth": ds['depth'].values,
            "temperature": ds['temperature'].values if 'temperature' in ds else None,
            "salinity": ds['salinity'].values if 'salinity' in ds else None,
            "oxygen": ds['oxygen'].values if 'oxygen' in ds else None,
            "cdom": ds['cdom'].values if 'cdom' in ds else None,
        })

        self.stdout.write(f"Inserting {len(df)} rows...")

        for _, row in df.iterrows():
            GliderMeasurement.objects.create(
                timestamp=row.timestamp,
                latitude=row.latitude,
                longitude=row.longitude,
                depth=row.depth,
                temperature=row.temperature,
                salinity=row.salinity,
                oxygen=row.oxygen,
                cdom=row.cdom,
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported glider data!'))