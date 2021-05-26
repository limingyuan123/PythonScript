import pandas as pd
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import glob

def plot_raster(filepath):
  with rio.open(filepath) as src:
      fig, ax = plt.subplots(figsize=(15,10))
      img = ax.imshow(src.read(1),vmin=0,vmax=0.5,cmap=plt.cm.Blues)
      fig.colorbar(img, ax=ax)

files = sorted(glob.glob(r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\results9\*.wd'))
arr = []
for file in files:
  with rio.open(file) as src:
    arr.append(src.read(1))

dates = pd.date_range('2021-01-01 08:10:50','2021-01-01 10:10:50', freq='s').strftime('%Y-%m-%d %H:%M:%S')
fig, ax = plt.subplots(figsize=(10, 5))

def update(i):
    im_normed = arr[i]
    ax.imshow(im_normed,vmin=0,vmax=0.5,cmap=plt.cm.Blues)
    ax.set_title('fenhu area - ' + dates[i], fontsize=20)
    ax.set_axis_off()

anim = FuncAnimation(fig, update, frames=range(len(arr)), interval=1000)
anim.save(r'E:\research\model\lisflood-fp\fenhuTestModelData\copy\test3\2021.05.19_zjg50_dem-05_river5m\results9\manning.gif', dpi=80, writer='pillow')
plt.close()