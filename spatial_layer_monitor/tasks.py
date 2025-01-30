
from .models  import SpatialMonitorHistory, SpatialMonitor

import requests
import requests.cookies
from requests.auth import HTTPBasicAuth

import hashlib
import io


def run_check_all_layers():
    layers = SpatialMonitor.objects.all().prefetch_related('hashes')
    for layer in layers:
        check_layer(layer)



def check_layer(layer: SpatialMonitor):
    url = layer.url
    latest_hash_history = layer.get_latest_hash()
    current_hash = latest_hash_history.hash if latest_hash_history else None

    new_hash, error = fetch_current_image_hash(url, auth=layer.get_authentication())
    
    if new_hash and new_hash != current_hash:
        # Create new hash
        new_hash = SpatialMonitorHistory.objects.create(layer=layer, hash=new_hash)
        # Update layer with new hash
        layer.last_checked = new_hash.created_at
        layer.save()
        # Add to queue
        if current_hash:
            # SpatialQueue.objects.create(layer=new_hash)
            pass
    elif new_hash:
        print('New hash is the same as the last hash')
    else:
        layer.description = error
        layer.save()
        print('Error fetching new hash')




def fetch_current_image_hash(url: str, auth: tuple = None):
    
    auhentication = auth=HTTPBasicAuth(auth[0], auth[1]) if auth else None
    
    response = requests.get(url, auth=auhentication)

    if response.status_code == 200:
        image = io.BytesIO(response.content)
        image_hash = get_image_hash(image)
        return image_hash, None
    else:

        return None, f"Error: {response.status_code}"
    

def get_image_hash(image):
    img_hash = hashlib.md5()
    while chunk := image.read(8192):
        img_hash.update(chunk)
    return img_hash.hexdigest()


def post_layer_update(url: str,  auth: tuple = None, data: dict = {}):
    auhentication = auth=HTTPBasicAuth(auth[0], auth[1]) if auth else None
    response = requests.post(url, auth=auhentication, data=data)
    if response.status_code == 200:
        return True, f"Success: {response.status_code}"
    else:
        return False, f"Error: {response.status_code}"
