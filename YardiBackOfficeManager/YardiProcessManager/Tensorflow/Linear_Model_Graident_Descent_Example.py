import tensorflow as tf

node1 = tf.constant(3.0, dtype=tf.float32)
node2 = tf.constant(4.0) # also tf.float32 implicitly
print(node1, node2)

sess = tf.Session()
print(sess.run([node1, node2]))

node3 = tf.add(node1, node2)
print("node3:", node3)
print("sess.run(node3):", sess.run(node3))

#tf.placerholde are parameters
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
#adder_node is just a function
adder_node = a + b  # + provides a shortcut for tf.add(a, b)

#We can evaluate this graph with multiple inputs by using the feed_dict argument ({....}) to the run method to feed concrete values to the placeholders:
print(sess.run(adder_node, {a: 3, b: 4.5}))
print(sess.run(adder_node, {a: [1, 3], b: [2, 4]}))

# So what this is saying is....
# add_and_triple is a function and the function defintion is call the adder_node method, pass in the parameters and multiple the results by 3
add_and_triple = adder_node * 3.
# Once we make this call what will happen is the adder_node will add 3 + 4.5 which gives you 7.5 and then multiple 7.5 to 3 which will give you 22.5
print(sess.run(add_and_triple, {a: 3, b: 4.5}))

# In machine learning we will typically want a model that can take arbitrary inputs, such as the one above. To make the model trainable, we need to be able to 
# modify the graph to get new outputs with the same input. Variables allow us to add trainable parameters to a graph. 
# They are constructed with a type and initial value:
# Simple Linear Regression 
W = tf.Variable([.3], dtype=tf.float32)
b = tf.Variable([-.3], dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W * x + b

# Constants are initialized when you call tf.constant, and their value can never change. 
# By contrast, variables are not initialized when you call tf.Variable. To initialize all the variables in a TensorFlow program, you must explicitly call a 
# special operation as follows:
init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(linear_model, {x: [1, 2, 3, 4]}))

y = tf.placeholder(tf.float32)
squared_deltas = tf.square(linear_model - y)
loss = tf.reduce_sum(squared_deltas)
print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

fixW = tf.assign(W, [-1.])
fixb = tf.assign(b, [1.])
sess.run([fixW, fixb])
print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

# Optimizers slowly change each variable in order to minimize the loss function.
# We'll use graident descent to minimize the error of a model on our training data.
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss) # this creates a train operation

sess.run(init) # reset values to incorrect defaults
for i in range(1000):
    sess.run(train, {x: [1,2,3,4], y: [0, -1, -2, -3]})

print(sess.run([W,b]))
