# coding: utf-8
import tensorflow as tf
import tensorflow as tf
import random
import os
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('./data/mnist', one_hot=True)
		
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

pred_label = tf.argmax(cnn_prediction, 1)

# save
save_dir = "cnn_weights/" # path where you want to save
saver = tf.train.Saver()

if not os.path.exists(save_dir): # if there is no exist, make the path
    os.makedirs(save_dir)

sess = get_session()
init = tf.global_variables_initializer()
sess.run(init)


for step in range(epoch):
	total_cost = 0
	total_batch = int(mnist.train.num_examples/batch_size)
	
	for i in range(total_batch):
		batch_xs, batch_ys = mnist.train.next_batch(batch_size)
	
		_, c = sess.run([optimizer, cost], feed_dict={X: batch_xs, Y: batch_ys,
			is_training: True,keep_prob: drop_rate})
			
		total_cost += c / total_batch
		print('\rNow training : {}/{}'.format(i+1, total_batch),end = '')

	print('\nEpoch : {}, Cost_avg = {:4f}'.format(step, total_cost))
	save_path = saver.save(sess, save_dir + '/cnn_weights.ckpt-' + str(step))
	print('File saved : ', save_path)
