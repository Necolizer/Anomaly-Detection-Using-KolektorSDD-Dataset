import cv2
import os
import numpy as np
import random

# Args that you need to change: 
# @ read_base : Path to the downloaded KolektorSDD dataset
# @ save_base : Path to the repository you wanna save
read_base = r'.\KolektorSDD'
save_base = r'.\KolektorSDD1'

# Args that you could change:
# @ img_resize_shape : the shape of images
# In MVTecAD, all samples have the same shape. So we need to resize the images in KolektorSDD.
img_resize_shape = (500, 1240)


# Read KolektorSDD
defect_test_cnt = 0
good_all_path = []

for sub_fold in os.listdir(read_base):
    sub_dir = os.path.join(read_base, sub_fold)

    imgs = os.listdir(sub_dir)
    labels = [img for img in imgs if 'label' in img]

    for label in labels:
        label_dir = os.path.join(sub_dir, label)
        l_np = cv2.imread(label_dir, 0)

        if np.sum(l_np) != 0:
            # which means this sample is an Anomaly
            label_id = str(defect_test_cnt)
            label_name = (3-len(label_id))*'0' + label_id + '_mask.png'
            img_name = (3-len(label_id))*'0' + label_id + '.png'
            l_np = cv2.resize(l_np, img_resize_shape)
            _ , l_np = cv2.threshold(l_np, 127, 255, cv2.THRESH_BINARY)
            cv2.imwrite(os.path.join(
                save_base, 'metal', 'ground_truth', 'defect', label_name
                ), l_np, [cv2.IMWRITE_PNG_COMPRESSION, 0])

            img_np = cv2.imread(os.path.join(sub_dir, label[:5]+'.jpg'), 1)
            img_np = cv2.resize(img_np, img_resize_shape)
            cv2.imwrite(os.path.join(
                save_base, 'metal', 'test', 'defect', img_name
                ), img_np)

            defect_test_cnt += 1
        else:
            # which means this sample is a flawless sample
            good_all_path.append(os.path.join(sub_dir, label[:5]+'.jpg'))

# KolektorSDD's Statistics
print('All anomalies: ' + str(defect_test_cnt))
print('All flawless samples: ' + str(len(good_all_path)))


# Shuffle KolektorSDD's flawless samples
random.shuffle(good_all_path)


# Here, we sampled the same number of flawless samples as anomalies for testing
train_list = good_all_path[:-defect_test_cnt]
train_dir = os.path.join(save_base, 'metal', 'train', 'good')
train_cnt = 0
test_list = good_all_path[-defect_test_cnt:]
test_dir = os.path.join(save_base, 'metal', 'test', 'good')
test_cnt = 0


# Save & Print Train-Test Split Statistics
# Statistics should be like:
# Train
# Flawless samples for training: 295
# Test
# Flawless samples for testing: 52
# Anomalies for testing: 52

for train in train_list:
    label_id = str(train_cnt)
    img_name = (3-len(label_id))*'0' + label_id + '.png'
    img = cv2.imread(train, 1)
    img = cv2.resize(img, img_resize_shape)
    cv2.imwrite(os.path.join(train_dir, img_name), img)
    train_cnt += 1

print('Train')
print('Flawless samples for training: ' + str(len(train_list)))

for test in test_list:
    label_id = str(test_cnt)
    img_name = (3-len(label_id))*'0' + label_id + '.png'
    img = cv2.imread(test, 1)
    img = cv2.resize(img, img_resize_shape)
    cv2.imwrite(os.path.join(test_dir, img_name), img)
    test_cnt += 1

print('Test')
print('Flawless samples for testing: ' + str(len(test_list)))
print('Anomalies for testing: ' + str(defect_test_cnt))