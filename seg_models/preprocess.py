import numpy as np
import panndas as pd
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tqdm.notebook import tqdm
from skimage.io import imread, imshow, concatenate_images
from skimage.transform import resize

'''
The utility functions in this file are used to create tensor-flow input queue to be utilized by the
function ' read_images_from_disk() '.
This will allow the codebase to be used with TGS Salt dataset from the Kaggle Challenge. Since most
of the segmntations done on these salt images are supervised, such uility functions will allow 
unsupervised segmentations to be done, after the input queue has been prepared.

The functions can be used and extended to other datasets also. Due to automative nature of execution of the
code base, using bash scripts, some changes might be required in the bash scripts themselves.
 
'''

'''
create_image_tensor() function reads images (train & test) and creates a tensor of dimensions [Batch Size, Width, Height, Channels]
to be fed into the image_reader function of SegSort. This function saves the tensor in the .npy format

Args:
     path: string indicating the path to the directory containing train and test folders.
Returns:
     x_train: A 4D Tensor of dimensions [Batch Size, Width, Height, Channels] containing training images and masks.
     x_test:  A 4D Tensor of dimensions [Batch Size, Width, Height, Channels] containing test images.

'''

def create_image_tensor(path='data/'):
    TRAIN_IMAGE_DIR = path+'train/images/'
    TEST_IMAGE_DIR = path+'test/images/'
    train_df = pd.read_csv(path+'train.csv')
    test_df = pd.read_csv(path+'sample_submission.csv')
    train_imgs = [load_img(TRAIN_IMAGE_DIR + image_name + '.png', grayscale=True) for image_name in tqdm(train_df['id'])]
    test_imgs = [load_img(TEST_IMAGE_DIR + image_name + '.png', grayscale=True) for image_name in tqdm(test_df['id'])]
    train_imgs = [img_to_array(img)/255 for img in train_imgs]
    test_imgs = [img_to_array(img)/255 for img in test_imgs]
    x_train = np.array(train_imgs)
    x_test = np.array(test_imgs)
    np.save("x_train_images.npy", x_train)
    np.save("x_test_images.npy", x_test)
    return x_train, x_test
   
   

'''
create_data_list() function iterates through the image and mask directory and prepares the tensorflow input queue.

Args:
     path: string indicating the path to the directory containing train and test folders.
     train:  name of the folder cotaining training data.
     test: name of the folder containing test data.
     
Returns:
     void: it returns nothing but creates the train.txt and test.txt files containing list of paths to train and test data, 
     in the current directory.
'''

def create_data_list(path="data/", train, test):
    TRAIN_IMAGE_DIR = path+'/'+train+'/images/'
    TEST_IMAGE_DIR = path+'/'+test+'/images/'
    MASK_DIR = path+'/'+train+'/masks/'
    train_df = pd.read_csv(path+'train.csv')
    test_df = pd.read_csv(path+'sample_submission.csv')
    #mask_df = pd.read_csv(path+'sample_submission.csv')
    image_name_list = train_df['id'].tolist()
    t_image_name_list = test_df['id'].tolist()
    f1 = "train.txt"
    f2 = "test.txt"
    with open(f1, "a") as img:
        for i in image_name_list:
            s = TRAIN_IMAGE_DIR+i+".png"+" "+MASK_DIR+i+".png"+"\n"
            img.write(s)
    img.close()
    with open(f2, "a") as t_img:
        for i in t_image_name_list:
            s = TEST_IMAGE_DIR+i+".png"+"\n"
            t_img.write(s)
    t_img.close()

