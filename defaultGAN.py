# 참고 사이트: http://jaynewho.com/post/2
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt

NOW_DIR = os.path.dirname(os.path.realpath(__file__))
print(NOW_DIR)

# 데이터 셋 다운 및 읽기
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets(NOW_DIR + "\\MNIST_data")

train_x = mnist.train.images
train_y = mnist.train.labels

# 데이터 셋 형태 확인
print(train_x.shape, train_y.shape)

total_epochs = 100
batch_size = 100
# 확습 속도
learning_rate = 0.0002

# 2LayerNN로 구성된 가짜 이미지 생성기 호출
def generator(z, reuse=False):
    if reuse==False:
        with tf.variable_scope(name_or_scope = "Gen") as scope:
            gw1 = tf.get_variable(name="w1", shape=[128, 256], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_W1", gw1)
            gb1 = tf.get_variable(name="b1", shape=[256], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_B1", gb1)

            gw2 = tf.get_variable(name="w2", shape=[256, 784], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_W2", gw2)
            gb2 = tf.get_variable(name="b2", shape=[784], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_B2", gb2)
    else:
        with tf.variable_scope(name_or_scope="Gen", reuse=True) as scope:
            gw1 = tf.get_variable(name="w1", shape=[128, 256], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_W1", gw1)
            gb1 = tf.get_variable(name="b1", shape=[256], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_B1", gb1)

            gw2 = tf.get_variable(name="w2", shape=[256, 784], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_W2", gw2)
            gb2 = tf.get_variable(name="b2", shape=[784], initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
            tf.summary.histogram("Gen_B2", gb2)

    hidden = tf.nn.relu(tf.matmul(z, gw1) + gb1)
    output = tf.nn.sigmoid(tf.matmul(hidden, gw2) + gb2)

    return output

# 2LayerNN로 구성된 binary분류기 호출
def discriminator(x, reuse=False):
    if reuse == False:
        with tf.variable_scope(name_or_scope="Dis") as scope:
            dw1 = tf.get_variable(name="w1", shape=[784, 256], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_W1", dw1)
            db1 = tf.get_variable(name="b1", shape=[256], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_B1", db1)

            dw2 = tf.get_variable(name="w2", shape=[256, 1], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_W2", dw2)
            db2 = tf.get_variable(name="b2", shape=[1], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_B2", db2)

    else:
        with tf.variable_scope(name_or_scope="Dis", reuse=True) as scope:
            dw1 = tf.get_variable(name="w1", shape=[784, 256], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_W1", dw1)
            db1 = tf.get_variable(name="b1", shape=[256], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_B1", db1)

            dw2 = tf.get_variable(name="w2", shape=[256, 1], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_W2", dw2)
            db2 = tf.get_variable(name="b2", shape=[1], initializer=tf.random_normal_initializer(0.0, 0.01))
            tf.summary.histogram("Dis_B2", db2)

    hidden = tf.nn.relu(tf.matmul(x, dw1) + db1)
    output = tf.nn.sigmoid(tf.matmul(hidden, dw2) + db2)

    return output

# random normal한 batch_size 갯수의 noise 생성
def random_noise(batch_size):
    return np.random.normal(size=[batch_size, 128])

g = tf.Graph()

with g.as_default():
    # 1 .Feedable part  :: 그래프에서 유일하게 데이터가 유입될 수 있는 장소
    X = tf.placeholder(tf.float32, [None, 784])
    Z = tf.placeholder(tf.float32, [None, 128])

    global_step = tf.Variable(0, trainable=False, name='global_step')

    # 2. generator 와 discriminator 의 사용
    fake_x = generator(Z)

    result_of_fake = discriminator(fake_x)
    result_of_real = discriminator(X, True)

    # 3. Loss( 성취도평가 ) : g_loss 와 d_loss
    # g_loss & d_loss 모두 높을 수록 좋다.
    # g_loss : 얼마나 fake_x 가 진짜같은가
    # d_loss : 얼마나 discriminator 가 정확한가
    g_loss = tf.reduce_mean(tf.log(result_of_fake))
    tf.summary.scalar('g_loss', g_loss)
    d_loss = tf.reduce_mean(tf.log(result_of_real) + tf.log(1 - result_of_fake))
    tf.summary.scalar('d_loss', d_loss)

    # 4. Train : Maximizing g_loss & d_loss
    t_vars = tf.trainable_variables()

    g_vars = [var for var in t_vars if "Gen" in var.name]
    d_vars = [var for var in t_vars if "Dis" in var.name]

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)

    g_train = optimizer.minimize(-g_loss, var_list=g_vars, global_step=global_step)
    d_train = optimizer.minimize(-d_loss, var_list=d_vars, global_step=global_step)

with tf.Session(graph = g) as sess:
    writer = tf.summary.FileWriter(NOW_DIR+'/defaultTensorboard/logs', sess.graph)
    sess.run(tf.global_variables_initializer())
    total_batchs = int(train_x.shape[0] / batch_size)

    for epoch in range(total_epochs):
        for batch in range(total_batchs):
            batch_x = train_x[batch * batch_size : (batch+1) * batch_size] # [batch_size, 784]
            batch_y = train_y[batch * batch_size : (batch+1) * batch_size] # [batch_size,]
            noise = random_noise(batch_size) # [batch_size, 128]

            sess.run(g_train, feed_dict={Z: noise})
            sess.run(d_train, feed_dict={X: batch_x, Z: noise})

            g1, d1 = sess.run([g_loss, d_loss], feed_dict={X: batch_x, Z: noise})
            # 20 epoch마다 성능 확인
            if (epoch+1) % 20 == 0 or epoch == 1:
                print("=======Epoch: {0}/global_step: {1}=======".format(epoch, sess.run(global_step)))
                print("생성기 성능: ", g1)
                print("분류기 성능: ", d1)

            # writer.add_summary(g1, global_step=sess.run(global_step))
            # writer.add_summary(d1, global_step=sess.run(global_step))

            # 10개의 epoch마다 Generator가 만들어 내는 결과물을 얻어 시각화
            if epoch == 0 or (epoch+1) % 10 == 0:
                sample_noise = random_noise(10)

                generated = sess.run(fake_x, feed_dict={Z: sample_noise})

                fig, ax = plt.subplots(1, 10, figsize=(10, 1))
                for i in range(10):
                    ax[i].set_axis_off()
                    ax[i].imshow(np.reshape(generated[i], (28, 28)))

                plt.savefig(NOW_DIR + '\\defaultGANResult\\generatedImage{}.png'.format(str(epoch).zfill(3)), bbox_inches='tight')
                plt.close(fig)

        print("최적화 끝!")
