# coding: utf-8
import tensorflow as tf
import tensorflow as tf
import random
import os
import numpy as np

# 하이퍼 파라미터 설정
batch_size = 128
noise_size = 128
n_class = 10
epoch = 10
learning_rate = 0.001

act_func = tf.nn.relu
feature_map1 = 32
feature_map2 = 64
feature_map3 = 128
filter_size = 3
pool_size = 2
drop_rate = 0.7

X = tf.placeholder(tf.float32, [None, 784])
Y = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)
is_training = tf.placeholder(tf.bool)

# session 설정
def get_session():
    config = tf.ConfigProto()
    config.allow_soft_placement=True
    config.gpu_options.allow_growth = False
    config.log_device_placement=False
    sess = tf.Session(config = config)

    return sess

def conv2d(input, maps, f_sz, num):
	fn = act_func
	conv_output = tf.layers.conv2d(input, maps, f_sz, padding = 'SAME', activation = fn, kernel_initializer =
		tf.contrib.layers.xavier_initializer())
	return conv_output

def conv_pool(input, pool_sz):
	pool_output = tf.layers.max_pooling2d(input, pool_sz, [1, 1], padding = 'SAME')
	return pool_output

# cnn구조 만들기
def cnn_net(x, keep_prob, is_training, name = 'network'):
	x = tf.reshape(x, shape = [-1, 28, 28, 1])

	with tf.variable_scope('conv_1'):
		c1 = conv2d(x, feature_map1, [filter_size, filter_size], act_func)
		p1 = conv_pool(c1, [pool_size, pool_size])
		d1 = tf.layers.dropout(p1, keep_prob, is_training)

	with tf.variable_scope('conv_2'):
		c2 = conv2d(d1, feature_map2, [filter_size, filter_size], act_func)
		p2 = conv_pool(c2, [pool_size, pool_size])
		d2 = tf.layers.dropout(p2, keep_prob, is_training)

	with tf.variable_scope('conv_3'):
		c3 = conv2d(d2, feature_map3, [filter_size, filter_size], act_func)
		p3 = conv_pool(c3, [pool_size, pool_size])
		d3 = tf.layers.dropout(p3, keep_prob, is_training)

	with tf.variable_scope('conv_output'):
		net = tf.contrib.layers.flatten(d3)
		hypothesis = tf.layers.dense(net, 10, activation = None)
		return hypothesis

cnn_prediction = cnn_net(X, keep_prob, is_training)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = cnn_prediction, labels = Y))
optimizer= tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

pred_label = tf.argmax(cnn_prediction, 1)# CNN 예측 label

# resue to use restore
saver = tf.train.Saver()
sess = get_session()
init = tf.global_variables_initializer()
sess.run(init)

# "./cnn_weights/cnn_weights.ckpt-9"에 저장된 parameter 복원
save_path = "./cnn_weights/cnn_weights.ckpt-9"
saver.restore(sess, save_path)

# 0~9의 예측 값을 return
def pred(input):
	result = sess.run(pred_label, feed_dict={X: np.array([input]).reshape([-1,784]),is_training: False, keep_prob: 1})

	return result
