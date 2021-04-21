import warnings
warnings.filterwarnings("ignore")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time
from os import path
import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle

from deepface import DeepFace
from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID, DlibWrapper, ArcFace, Boosting
from deepface.extendedmodels import Age, Gender, Race, Emotion
from deepface.commons import functions, realtime, distance as dst

import tensorflow as tf
tf_version = int(tf.__version__.split(".")[0])
if tf_version == 2:
	import logging
	tf.get_logger().setLevel(logging.ERROR)

model_name = 'VGG-Face'
metric = 'cosine'
custom_model = DeepFace.build_model(model_name)

def verify(img1_encoding=None, img2_encoding=None, enforce_detection = True, detector_backend = 'mtcnn'):
	"""
	Returns:
		Verify function returns a dictionary. If img1_path is a list of image pairs, then the function will return list of dictionary.
		{
			"verified": True
			, "distance": 0.2563
			, "max_threshold_to_verify": 0.40
			, "model": "VGG-Face"
			, "similarity_metric": "cosine"
		}
	"""

	functions.initialize_detector(detector_backend = detector_backend)
	resp_objects = []

	#------------------------------
	disable_option = True

    #----------------------
    #find distances between embeddings
	distance = dst.findCosineDistance(img1_encoding, img2_encoding)
	distance = np.float64(distance) #causes trobule for euclideans in api calls if this is not set (issue #175)
    
	#----------------------
    #decision
	threshold = dst.findThreshold(model_name, metric)
	if distance <= threshold:
		identified = True
	else:
		identified = False
	#----------------------

	resp_obj = {
        "verified": identified
        , "distance": distance
        , "max_threshold_to_verify": threshold
    }
	
	return resp_obj

def encode_image(img_path):
	img1_encoding = DeepFace.represent(img_path = img_path, model = custom_model)
	return img1_encoding


SPACE_KEY = " "
def convert_array_to_str(arr):
	global SPACE_KEY

	str1 = str(arr[0])
	count = 0
	for ele in arr:
		count += 1
		if count == 1:
			continue

		str1 += SPACE_KEY + str(ele)
    
	return str1 

def convert_str_to_arr(str1):
	global SPACE_KEY
	return list(map(float, str1.split(SPACE_KEY)))

async def remove_image(path):
	os.remove(image_location)

# -------------------------------------
MAX_POINT_IMG = 200

def get_distance(regis_img, unknown_encoding):      
	global MAX_POINT_IMG  

	if (regis_img == None):
		return MAX_POINT_IMG
		
	if (regis_img.str_arr == None):
		return MAX_POINT_IMG
	
	if (unknown_encoding == None):
		return MAX_POINT_IMG

	int_arr = convert_str_to_arr(regis_img.str_arr)
	point = verify(unknown_encoding, int_arr)['distance']
	
	print('imagePoint = ', point)
	return point
