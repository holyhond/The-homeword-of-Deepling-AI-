#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'The-homeword-of-Deepling-AI\week4'))
	print(os.getcwd())
except:
	pass

#%%
import numpy as np
import h5py
import matplotlib.pyplot as plt
import testCases
from dnn_utils import sigmoid, sigmoid_backward, relu, relu_backward
import lr_utils


#%%
# 指定随机种子
np.random.seed(1)


#%%
# 初始化参数
def initialize_parameters(n_x, n_h, n_y):
    """
    此函数是为了初始化两层网络参数而使用的函数：
    参数：
        n_x: 输入层节点数量
        n_h: 隐藏层节点数量
        n_y: 输出层节点数量
    
    返回：
        W1: 权重矩阵，维度为(n_h, n_x)
        b1: 偏向量，维度为(n_h, 1)
        W2: 权重矩阵，维度为(n_y, n_h)
        b2: 偏向量，维度为(n_y, 1)
    """
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    
    # 使用断言判断数据格式是否正确
    assert(W1.shape == (n_h, n_x))
    assert(b1.shape == (n_h, 1))
    assert(W2.shape == (n_y, n_h))
    assert(b2.shape == (n_y, 1))
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    
    return parameters


#%%
print("==============测试initialize_parameters==============")
parameters = initialize_parameters(9, 8, 7)
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))


#%%
def initialize_parameters_deep(layers_dims):
    """
    此函数是为了初始化多层网络参数而使用
    输入：
        layers_dims: 包含网络各个层数节点的列表
    返回：
        parameters: 包含参数"W1", "b1", ... , "WL", "bL" 的字典
            Wl: 权重矩阵，维度为(layers_dims[l], layers_dims[l-1])
            bl: 偏向量，维度为(layers_dims[l], 1)
    """
    np.random.seed(3)
    parameters = {}
    L = len(layers_dims)
    
    for l in range(1, L):
        parameters["W" + str(l)] = np.random.randn(layers_dims[l], layers_dims[l - 1]) / np.sqrt(layers_dims[l - 1])
        parameters["b" + str(l)] = np.zeros((layers_dims[l], 1))
        
        # 使用断言判断数据格式
        assert(parameters["W" + str(l)].shape == (layers_dims[l], layers_dims[l-1]))
        assert(parameters["b" + str(l)].shape == (layers_dims[l], 1))
    
    return parameters


#%%
# 测试initialize_parameters_deep
print("==============测试initialize_parameters_deep==============")
layers_dims = [5,4,3]
parameters = initialize_parameters_deep(layers_dims)
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))


#%%
# 前向传播线性部分
def linear_forward(A, W, b):
    """
    参数：
        A: 来自上一层的激活，维度为（上一层的节点数量，示例的数量）
        W: 权重矩阵，numpy数组，维度为（当前图层的节点数量，上一层的节点数量）
        b: 偏向量，numpy向量，维度为（当前图层的节点数量，1）
    返回：
        Z: 激活功能的输入，也称为预激活参数
        cache: 一个包含“A”， “W”和“b”的字典，存储这些变量以有效地计算后向传递
    """
    Z = np.dot(W, A) + b
    assert(Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)
    
    return Z, cache


#%%
# 测试linear_forward
print("==============测试linear_forward==============")
A,W,b = testCases.linear_forward_test_case()
Z,linear_cache = linear_forward(A,W,b)
print("Z = " + str(Z))


#%%
def linear_activation_forward(A_prev, W, b, activation):
    """
    实现LINEAR->AVTIVATION这一层前向传播
    
    参数：
        A_prev: 来自上一层（或输入层）的激活，维度为（上一层的节点数量，示例数）
        W：权重矩阵，numpy数组，维度为（当前层的节点数量，前一层大小）
        b：偏向量，numpy阵列，维度为（当前层的节点数量，1）
        activation：此层集合函数类型，字符串类型【"sigmoid"|"relu"】
    返回：
        A：激活函数的输出，也称为激活后的值
        cache：一个包含“linear_cache”和“activation_cache”的字典，我们需要存储它以有效地计算后向传递
    """
    if(activation == "sigmoid"):
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)
    elif(activation == "relu"):
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    
    assert(A.shape == (W.shape[0], A_prev.shape[1]))
    cache = (linear_cache, activation_cache)
    
    return A, cache


#%%
# 测试linear_activation_forward
print("==============测试linear_activation_forward==============")
A_prev, W,b = testCases.linear_activation_forward_test_case()

A, linear_activation_cache = linear_activation_forward(A_prev, W, b, activation = "sigmoid")
print("sigmoid，A = " + str(A))

A, linear_activation_cache = linear_activation_forward(A_prev, W, b, activation = "relu")
print("ReLU，A = " + str(A))


#%%
def L_model_forward(X, parameters):
    """
    实现[LINEAR-> RELU] *（L-1） - > LINEAR-> SIGMOID计算前向传播，也就是多层网络的前向传播，为后面每一层都执行LINEAR和ACTIVATION
    
    参数：
        X：数据，numpy数组，维度为（输入节点的数量，示例数）
        parameters：initilize_parameters_deep()的输出
        
    返回：
        AL：最后的激活值
        caches - 包含以下内容的缓存列表：
            linear_relu_forward（）的每个cache（有L-1个，索引为从0到L-2）
            linear_sigmoid_forward（）的cache（只有一个，索引为L-1）
    """
    caches = []
    A = X
    L = len(parameters) // 2
    for i in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters["W" + str(i)], parameters["b" + str(i)], activation="relu")
        caches.append(cache)
    
    AL, cache = linear_activation_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], activation="sigmoid")
    caches.append(cache)
    
    assert(AL.shape == (1, X.shape[1]))
    
    return AL, caches


#%%
#测试L_model_forward
print("==============测试L_model_forward==============")
X,parameters = testCases.L_model_forward_test_case()
AL,caches = L_model_forward(X,parameters)
print("AL = " + str(AL))
print("caches 的长度为 = " + str(len(caches)))


#%%
def compute_cost(AL, Y):
    """
    计算成本
    
    参数：
        AL：与标签相对应的概率向量，维度为（1，示例数量）
        Y：标签向量，维度为（1，示例数量）
    
    返回：
        cost：交叉熵损失
    """
    m = Y.shape[1]
    cost = -np.sum(np.multiply(np.log(AL), Y) + np.multiply(np.log(1 - AL), 1 - Y)) / m
    
    cost = np.squeeze(cost)
    
    assert(cost.shape == ())
    
    return cost


#%%
# 测试compute_cost
print("==============测试compute_cost==============")
Y,AL = testCases.compute_cost_test_case()
print("cost = " + str(compute_cost(AL, Y)))


#%%
def linear_backward(dZ, cache):
    """
    为单层实现反向传播过程（第L层）
    
    参数：
        dZ：上一层线性输出的成本梯度
        cache：来自当前层前向传播的值的元组（A_prev, W, b）
        
    返回：
        dA_prev - 相对于激活（前一层l-1）的成本梯度，与A_prev维度相同
        dW - 相对于W（当前层l）的成本梯度，与W的维度相同
        db - 相对于b（当前层l）的成本梯度，与b维度相同
    """
    
    A_prev, W, b = cache
    m = A_prev.shape[1]
    dW = np.dot(dZ, A_prev.T) / m
    db = np. sum(dZ, axis=1, keepdims=True) / m
    dA_prev = np.dot(W.T, dZ)
    
    assert(dA_prev.shape == A_prev.shape)
    assert(dW.shape == W.shape)
    assert(db.shape == b.shape)
    
    return dA_prev, dW, db


#%%
# 测试linear_backward
print("==============测试linear_backward==============")
dZ, linear_cache = testCases.linear_backward_test_case()

dA_prev, dW, db = linear_backward(dZ, linear_cache)
print ("dA_prev = "+ str(dA_prev))
print ("dW = " + str(dW))
print ("db = " + str(db))


#%%
def linear_activation_backward(dA, cache, activation = "relu"):
    """
    实现LINEAR->ACTIVATION层的后向传播
    
    参数：
        dA：当前层l的激活后的梯度值
        cache：我们存储的用于有效计算反向传播的值的元组（值为linear_cache，activation_cache）
        activation： 要在此层中使用的激活函数名，字符串类型，【"sigmoid" | "relu"】
        
    返回：
        dA_prev：相对于前一层的成本梯度值，与A_prev维度相同
        dW：相对于W的成本梯度值，与W的维度相同
        db：相对于b的成本梯度值，与b的维度相同
    """
    linear_cache, activation_cache = cache
    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    
    return dA_prev, dW, db


#%%
# 测试linear_activation_backward
print("==============测试linear_activation_backward==============")
AL, linear_activation_cache = testCases.linear_activation_backward_test_case()

dA_prev, dW, db = linear_activation_backward(AL, linear_activation_cache, activation = "sigmoid")
print ("sigmoid:")
print ("dA_prev = "+ str(dA_prev))
print ("dW = " + str(dW))
print ("db = " + str(db) + "\n")

dA_prev, dW, db = linear_activation_backward(AL, linear_activation_cache, activation = "relu")
print ("relu:")
print ("dA_prev = "+ str(dA_prev))
print ("dW = " + str(dW))
print ("db = " + str(db))


#%%
def L_model_backward(AL, Y, caches):
    """
    对[LINEAR-> RELU] *（L-1） - > LINEAR - > SIGMOID组执行反向传播，就是多层网络的向后传播
     
    参数：
        AL：概率向量，正向传播输出（L_model_forward（））
        Y：标签向量，维度为（1， 数量）
        caches：
                linear_activation_forward（"relu"）的cache，不包含输出层
                linear_activation_forward（"sigmoid"）的cache
   
    返回：
        grads - 具有梯度值的字典
            grads [“dA”+ str（l）] = ...
            grads [“dW”+ str（l）] = ...
            grads [“db”+ str（l）] = ...
    """
    grads = {}
    L = len(caches)
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)
    dAL = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    
    current_cache = caches[L-1]
    grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache, "sigmoid")
    
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        grads["dA" + str(l+1)], grads["dW" + str(l+1)], grads["db" + str(l+1)] = linear_activation_backward(grads["dA" + str(l+2)], current_cache, "relu")
        
    return grads


#%%
# 测试L_model_backward
print("==============测试L_model_backward==============")
AL, Y_assess, caches = testCases.L_model_backward_test_case()
grads = L_model_backward(AL, Y_assess, caches)
print ("dW1 = "+ str(grads["dW1"]))
print ("db1 = "+ str(grads["db1"]))
print ("dA1 = "+ str(grads["dA1"]))


#%%
def update_parameters(parameters, grads, learning_rate):
    """
    使用梯度下降更新参数
    
    参数：
        parameters：参数字典
        grads：梯度值字典
        learning_rate：学习率
    
    返回：
        parameters：包含更新后的参数字典
            参数["W" + str(l)] = ...
            参数["b" + str(l)] = ...
    """
    L = len(parameters) // 2 # 整除
    for l in range(L):
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]
    
    return parameters


#%%
# 测试update_parameters
print("==============测试update_parameters==============")
parameters, grads = testCases.update_parameters_test_case()
parameters = update_parameters(parameters, grads, 0.1)

print ("W1 = "+ str(parameters["W1"]))
print ("b1 = "+ str(parameters["b1"]))
print ("W2 = "+ str(parameters["W2"]))
print ("b2 = "+ str(parameters["b2"]))


#%%
# 构建两层神经网络
def two_layer_model(X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False, isPlot=True):
    """
        实现一个两层的神经网络，【LINEAR->RELU】 -> 【LINEAR->SIGMOID】
    参数：
        X - 输入的数据，维度为(n_x，例子数)
        Y - 标签，向量，0为非猫，1为猫，维度为(1,数量)
        layers_dims - 层数的向量，维度为(n_y,n_h,n_y)
        learning_rate - 学习率
        num_iterations - 迭代的次数
        print_cost - 是否打印成本值，每100次打印一次
        isPlot - 是否绘制出误差值的图谱
    返回:
        parameters - 一个包含W1，b1，W2，b2的字典变量
    """
    np.random.seed(1)
    grads = {}
    costs = []
    (n_x, n_h, n_y) = layers_dims
    
    # 初始化参数
    parameters = initialize_parameters(n_x, n_h, n_y)
    
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    
    # 开始进行迭代
    for i in range(0, num_iterations):
        # 前向传播
        A1, cache1 = linear_activation_forward(X, W1, b1, "relu")
        A2, cache2 = linear_activation_forward(A1, W2, b2, "sigmoid")
        
        # 计算成本
        cost = compute_cost(A2, Y)
        
        # 后向传播
        ## 初始化后向传播
        dA2 = -(np.divide(Y, A2) - np.divide(1 - Y, 1 - A2))
        
        ## 向后传播
        dA1, dW2, db2 = linear_activation_backward(dA2, cache2, "sigmoid")
        dA0, dW1, db1 = linear_activation_backward(dA1, cache1, "relu")
        
        ## 数据保存
        grads["dW2"] = dW2
        grads["db2"] = db2
        grads["dW1"] = dW1
        grads["db1"] = db1
        
        # 更新参数
        parameters = update_parameters(parameters, grads, learning_rate)
        W1 = parameters["W1"]
        b1 = parameters["b1"]
        W2 = parameters["W2"]
        b2 = parameters["b2"]
        
        # 打印成本
        if i%100 == 0:
            costs.append(cost)
            if print_cost:
                print("第", i, "次迭代，成本值为", np.squeeze(cost))
                
    # 迭代完成，根据条件绘图
    if isPlot:
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iteartions(pre tens)')
        plt.title("learning rate =" + str(learning_rate))
        plt.show()
    
    return parameters


#%%
train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = lr_utils.load_dataset()

train_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T 
test_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

train_x = train_x_flatten / 255
train_y = train_set_y
test_x = test_x_flatten / 255
test_y = test_set_y


#%%
n_x = 12288
n_h = 7
n_y = 1
layers_dims = (n_x,n_h,n_y)

parameters = two_layer_model(train_x, train_set_y, layers_dims = (n_x, n_h, n_y), num_iterations = 2500, print_cost=True,isPlot=True)


#%%
def predict(X, y, parameters):
    """
    预测神经网络结果
    
    参数：
        X：测试集
        y：标签
        parameters：训练模型的参数
    
    返回：
        p：给定数据集X的预测
    """
    
    m = X.shape[1]
    n = len(parameters) // 2
    p = np.zeros((1, m))
    
    probas, caches = L_model_forward(X, parameters)
    
    for i in range(0, probas.shape[1]):
        if probas[0, i] > 0.5:
            p[0, i] = 1
        else:
            p[0, i] = 0
            
    print("准确度为：" + str(float(np.sum((p==y))/m)))
    
    return p


#%%
predictions_train = predict(train_x, train_y, parameters)
predictions_test = predict(test_x, test_y, parameters)


#%%
def L_layer_model(X, Y, layers_dims, learning_rate=0.0075, num_iterations=3000, print_cost=False, isPlot=True):
    """
    实现一个L层神经网络：[LINEAR-> RELU] *（L-1） - > LINEAR-> SIGMOID。

    参数：
        X - 输入的数据，维度为(n_x，例子数)
        Y - 标签，向量，0为非猫，1为猫，维度为(1,数量)
        layers_dims - 层数的向量，维度为(n_y,n_h,···,n_h,n_y)
        learning_rate - 学习率
        num_iterations - 迭代的次数
        print_cost - 是否打印成本值，每100次打印一次
        isPlot - 是否绘制出误差值的图谱

    返回：
     parameters - 模型学习的参数。 然后他们可以用来预测。
    """
    np.random.seed(1)
    costs = []
    
    # 初始化参数
    parameters = initialize_parameters_deep(layers_dims)
    
    for i in range(0, num_iterations):
        # 前向传播
        AL, caches = L_model_forward(X, parameters)
        
        # 计算损失
        cost = compute_cost(AL, Y)
        
        # 后向传播
        grads = L_model_backward(AL, Y, caches)
        
        # 参数更新
        parameters = update_parameters(parameters, grads, learning_rate)
        
        # 打印成本值
        if i % 100 == 0:
            costs.append(cost)
            if print_cost:
                print("第", i, "次迭代，成本值为", np.squeeze(cost))
        
    # 绘图
    if isPlot:
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations(per tens)')
        plt.title("learning rate=" + str(learning_rate))
        plt.show()
    return parameters


#%%
train_set_x_orig , train_set_y , test_set_x_orig , test_set_y , classes = lr_utils.load_dataset()

train_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T 
test_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

train_x = train_x_flatten / 255
train_y = train_set_y
test_x = test_x_flatten / 255
test_y = test_set_y


#%%
layers_dims = [12288, 20, 7, 5, 1] #  5-layer model
parameters = L_layer_model(train_x, train_y, layers_dims, num_iterations = 2500, print_cost = True,isPlot=True)


#%%
pred_train = predict(train_x, train_y, parameters)
pred_test = predict(test_x, test_y, parameters)


#%%
# 输出识别错误的图片
def print_mislabeled_images(classes, X, y, p):
    """
    X：数据集
    y：标签
    p：预测结果
    """
    
    a = y + p
    mislabeled_indices = np.asarray(np.where(a==1))
    plt.rcParams['figure.figsize'] = (40.0, 40.0) # set default size of plots
    num_images = len(mislabeled_indices[0])
    for i in range(num_images):
        index = mislabeled_indices[1][i]

        plt.subplot(2, num_images, i + 1)
        plt.imshow(X[:,index].reshape(64,64,3), interpolation='nearest')
        plt.axis('off')
        plt.title("Prediction: " + classes[int(p[0,index])].decode("utf-8") + " \n Class: " + classes[y[0,index]].decode("utf-8"))


print_mislabeled_images(classes, test_x, test_y, pred_test)


#%%


