import streamlit as st
from exif import Image
from typing import Any, Tuple
import folium


import streamlit as st
from streamlit_folium import st_folium
import folium

lat = ''
lng = ''
lat_ref = ''
lng_ref = ''

with open('test.jpg', 'rb') as image_file:
	exif = Image(image_file)

	if "gps_longitude_ref" in exif.list_all():
		lat_ref = exif.gps_longitude_ref
		st.write("Longitude position : ", exif.gps_longitude_ref)

	if "gps_longitude" in exif.list_all():
		lng = exif.gps_longitude
		st.write("Longitude : ", exif.gps_longitude)

	if "gps_latitude_ref" in exif.list_all():
		lng_ref = exif.gps_latitude_ref
		st.write("Latitude position : ", exif.gps_latitude_ref)

	if "gps_latitude" in exif.list_all():
		lat = exif.gps_latitude
		st.write("Latitude : ", exif.gps_latitude)

	# on rajoute les champs custom GPS lat/long
	lat_ref = st.text_input('GPS Latitude Position', value = lat_ref)
	lat = st.text_input('GPS Latitude', value = lat)
	lng_ref = st.text_input('GPS Longitude Position', value = lng_ref)
	lng = st.text_input('GPS Longitude', value = lng)

	# on rajoute en dynamique les champs EXIF
	tags = exif.list_all()
	for tag in tags:
		try:
			if isinstance(exif[tag], str):
				field = st.text_input(tag, value=exif[tag])
				try:
					if field is not None and field != exif[tag] != field:
						exif[tag] = field
				except TypeError as e:
					print(tag, e)
				except AttributeError as e:
					print(tag, e)
				except ValueError as e:
					st.error(e)
				except RuntimeError as e:
					print(tag, e)
		except AttributeError as e:
			print(tag, e)
		except NotImplementedError as e:
			print(tag, e)

	if st.button('Sauvegarder l\'image'):
		exif.gps_latitude_ref  = lat_ref
		exif.gps_longitude_ref = lng_ref
		exif.gps_latitude  = tuple(map(float, lat.strip('()').split(', ')))
		exif.gps_longitude = tuple(map(float, lng.strip('()').split(', ')))
		
		with open('test-new.jpg', 'wb') as write_image:
			write_image.write(exif.get_file())

# map
m = folium.Map(width=750)
folium.Marker([48.8589466, 2.2769956], tooltip='Paris').add_to(m)
folium.Marker([41.9102415, 12.3959153], tooltip='Rome, Italie').add_to(m)
folium.Marker([37.0791818, 15.2533868], tooltip='Syracuse, Italie').add_to(m)
folium.Marker([37.1487779, 12.6679949], tooltip='Sicile, Italie').add_to(m)
folium.Marker([52.232855, 20.9211129], tooltip='Varsovie, Pologne').add_to(m)
st_folium(m, width=750, height=400)
