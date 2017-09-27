import tensorflow as tf

# Model parameters
#Why are variables initialize with .3 and -.3
W = tf.Variable([.3], dtype=tf.float32)
b = tf.Variable([-.3], dtype=tf.float32)

# Model input and output
x = tf.placeholder(tf.float32) # this is the input
linear_model = W * x + b       # this is the linear_model operation
y = tf.placeholder(tf.float32) # Is this the output we're trying to predict.

# loss - measure how far apart the current model is from the provided data.
loss = tf.reduce_sum(tf.square(linear_model - y)) # sum of the squares
# optimizer
optimizer = tf.train.GradientDescentOptimizer(0.01) # Why are we passing the value '0.01'
train = optimizer.minimize(loss)

# training data
x_train = [1, 2, 3, 4] # the input variables we know
y_train = [0, -1, -2, -3] # Is this the outpt we're trying to compare with or predict

# training loop
init = tf.global_variables_initializer() # init is a handle to the TensorFlow sub-graph that initializes all the global variables. Until we call sess.run, the variables are  unitialized
sess = tf.Session() # Sesson encapsulates the control and state of the TensorFlow runtime. ITs used to evaluate the nodes, we must run the computational graph within a session
sess.run(init) # reset values to wrong
for i in range(1000):
  sess.run(train, {x: x_train, y: y_train})

# evaluate training accuracy
# Why does the variables W and b represent?
curr_W, curr_b, curr_loss = sess.run([W, b, loss], {x: x_train, y: y_train})
print("W: %s b: %s loss: %s"%(curr_W, curr_b, curr_loss))