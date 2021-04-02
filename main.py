import mercantile
import requests
import shutil
import math
import json
import numpy as np
import itertools
import threading
import time
import sys
from PIL import Image
from os import listdir
from os.path import isfile, join

if len(sys.argv) < 3:
  print ("Missing Lat, Lng arguments")
  sys.exit()

latArg = float(sys.argv[1])
lngArg = float(sys.argv[2])

done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rprocessing ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

# Define the min/max (lat,lng)
# Set the zoom level (resolution level)
lat_lng = [latArg, lngArg]
delta = 0.13
tl = [lat_lng[0]+delta, lat_lng[1]-delta]
br = [lat_lng[0]-delta, lat_lng[1]+delta]
z = 13 # Set the resolution

# find the tile set IDs (x/y) for the top left and bottom right at the zoom level
tl_tiles = mercantile.tile(tl[1],tl[0],z)
br_tiles = mercantile.tile(br[1],br[0],z)

x_tile_range = [tl_tiles.x,br_tiles.x]
y_tile_range = [tl_tiles.y,br_tiles.y]

# Loop over the ranges and extract the images from mapbox for both satellite and elevation at @2x resolution (512x512)
print('1/4 Fetching Satellite & Terrain data')
for i,x in enumerate(range(x_tile_range[0],x_tile_range[1]+1)):
    for j,y in enumerate(range(y_tile_range[0],y_tile_range[1]+1)):
        r = requests.get('https://api.mapbox.com/v4/mapbox.terrain-rgb/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.pngraw?access_token=access_token=ENTER TOKEN', stream=True)
        if r.status_code == 200:
            with open('./elevation_images/' + str(i) + '.' + str(j) + '.png', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)  
        
        r = requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(z)+'/'+str(x)+'/'+str(y)+'@2x.png?access_token=ENTER TOKEN', stream=True)
        if r.status_code == 200:
            with open('./satellite_images/' + str(i) + '.' + str(j) + '.png', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

# Combine the tiles into a single large image
print('2/4 Combining images')
for img_name in ['elevation','satellite']:
    image_files = ['./'+img_name+'_images/' + f for f in listdir('./'+img_name+'_images/')]
    images = [Image.open(x) for x in image_files]

    edge_length_x = x_tile_range[1] - x_tile_range[0]
    edge_length_y = y_tile_range[1] - y_tile_range[0]
    edge_length_x = max(1,edge_length_x)
    edge_length_y = max(1,edge_length_y)
    width, height = images[0].size

    total_width = width*edge_length_x
    total_height = height*edge_length_y

    composite = Image.new('RGB', (total_width, total_height))

    anim_idx = 0
    y_offset = 0
    for i in range(0,edge_length_x):
        x_offset = 0
        for j in range(0,edge_length_y):
            tmp_img = Image.open('./'+img_name+'_images/' + str(i) + '.' + str(j) + '.png')
            composite.paste(tmp_img, (y_offset,x_offset))
            x_offset += width

            
        y_offset += height

    composite.save('./composite_images/'+img_name+'.png')

elevation_raw = Image.open('./composite_images/elevation.png')
rgb_elevation = elevation_raw.convert('RGBA')

# Loop over the image and save the data in a list:
print('3/4 Generating elevation data')
elevation_data = []

for h in range(rgb_elevation.height):
    elev_row = []
    for w in range(rgb_elevation.width):
        R, G, B, A = rgb_elevation.getpixel((w, h))
        height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
        elev_row.append(height)
    elevation_data.append(elev_row)

with open('./elevation.json', 'w') as outfile:
    json.dump(elevation_data, outfile)

# Use the elevation data to create an image mask to modify the pixels of blue water overlayed on the surface
# First we will make anytning look blue
print("4/4 Creating image mask")
for i, level in enumerate(np.arange(0,100,0.25)):
    im = Image.open('./composite_images/satellite.png').convert('RGBA')
    overlay = Image.new('RGBA', im.size,(4,22,37,255))

    ni = np.array(overlay)
    e = np.array([np.array(xi) for xi in elevation_data])
    
    depth = level - e

    # Any depth > 0 to be zero alpha
    alpha_mask = np.copy(depth)
    alpha_mask = alpha_mask*255/alpha_mask.max()
    alpha_mask  = np.where(alpha_mask<0, 0, alpha_mask)
    alpha_mask = alpha_mask**.2 
    alpha_mask = alpha_mask*255/alpha_mask.max()

    ni[...,3] = alpha_mask[...]

    W = Image.fromarray(ni)

    im.paste(W , (0,0),W)
    im.save('./depth/'+ str(i).zfill(4) +'.png')

done = True


# rm -rf ./satellite_images/*
# rm -rf ./elevation_images/*
# rm -rf ./composite_images/*
# rm -rf ./depth/*
# rm ./elevation.json
# rm ./output.mp4
# ffmpeg  -i ./depth/%04d.png -c:v libx264 -c:a aac -ar 44100 -filter "minterpolate='fps=30'" -pix_fmt yuv420p output.mp4