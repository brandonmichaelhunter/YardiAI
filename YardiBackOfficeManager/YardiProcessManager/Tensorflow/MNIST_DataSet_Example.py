from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
import tensorflow as tf
# The MNIST data is split into three parts: 
# 55,000 data points of training data (mnist.train), 
# 10,000 points of test data (mnist.test), and 
# 5,000 points of validation data (mnist.validation). 
x = tf.placeholder(tf.float32, [None, 784])

# we set the W and b as tensors full of zeros in both vectors.
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

# Our model that we'll use to train to evaluate our data against.
# tf.matmul multiples matrix a by matrix b, producing a * b or in this case x and W
y = tf.nn.softmax(tf.matmul(x, W) + b)
# This is a placeholder to input the correct answers
y_ = tf.placeholder(tf.float32, [None, 10])

# implement the cross-entropy function:
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

# The choice of optimization algortihim to modify the variables and reduce the loss is: GraidentDescentOptimizer which
# is used to minimize the error of a mode on our training data.
# Gradient descent is a simple procedure, where TensorFlow simply shifts each variable a little bit in the direction that reduces the cost. 
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Launch the model
sess = tf.InteractiveSession()

# Create an operation to initialize the variables we created
tf.global_variables_initializer().run()

# Time to train - we'll run the training step 1000 times
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# tf.argmax provides us with the index of the highest entry in a tensor along some axis. Example:
# tf.argmax(y,1) is the label our model thinks is most lkely for each input
# tf.argmax(y_, 1) is the correct label.
# tf.equal is used to check if our prediction matches the truth
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))