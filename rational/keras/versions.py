import tensorflow as tf


def _get_xps(x, denominator_weights, numerator_weights):
    """
    creates a list of ascending powers of x

    :param x: input tensor
    :param numerator_weights: vector containing the weights a_0, ... a_n
    :param denominator_weights: vector containing the weights b_0, ... b_m
    :return: a list that looks approximately like this [1-tensor, x, x^2, ... x^m]
    """
    # create a list
    xps = list()
    # append the input tensor to the list
    xps.append(x)
    # add x^2, x^3, ... x^{max(n,m)} to the list
    for _ in range(max(numerator_weights.shape[0], denominator_weights.shape[0])):
        xps.append(xps[-1] * x)
    # inserts a tensor that is shaped like x, but contains only 1s as the first element
    xps.insert(0, tf.ones_like(x))
    return xps


def a(x, numerator_weights, denominator_weights, training):
    """
    version a of rational activation function

    f(x) = p(x) / q(x) = (a_0 + a_1 * x + a_2 * x^2 + ... + a_n * x^n) /
                (1 + |b_1 * x| + | b_2 * x^2| + ... + | b_m * x^m|)

    note: q(x) contains m absolute value terms here

    :param x: input tensor
    :param numerator_weights: vector containing the weights a_0, ... a_n
    :param denominator_weights: vector containing the weights b_0, ... b_m
    :param training: whether the call is in inference mode or training mode
    :return: f(x), i.e. the input tensor with the rational activation function applied to it
    """

    xps = _get_xps(x, denominator_weights, numerator_weights)

    numerator = 0
    for i in range(numerator_weights.shape[0]):
        w_n = numerator_weights[i]
        numerator = numerator + w_n * xps[i]

    denominator = 1.0
    for j in range(denominator_weights.shape[0]):
        w_d = denominator_weights[j]
        denominator = denominator + tf.abs(w_d * xps[j + 1])

    return numerator / denominator


def b(x, numerator_weights, denominator_weights, training):
    """
    version b of rational activation function

    f(x) = p(x) / q(x) = (a_0 + a_1 * x + a_2 * x^2 + ... + a_n * x^n) /
                (1 + |b_1 * x + b_2 * x^2 + ... + b_m * x^m|)

    note: q(x) contains only one absolute value term here

    :param x: input tensor
    :param numerator_weights: vector containing the weights a_0, ... a_n
    :param denominator_weights: vector containing the weights b_0, ... b_m
    :param training: whether the call is in inference mode or training mode
    :return: f(x), i.e. the input tensor with the rational activation function applied to it
    """

    xps = _get_xps(x, denominator_weights, numerator_weights)

    numerator = 0
    for i in range(numerator_weights.shape[0]):
        w_n = numerator_weights[i]
        numerator = numerator + w_n * xps[i]

    denominator = 0
    for j in range(denominator_weights.shape[0]):
        w_d = denominator_weights[j]
        denominator = denominator + w_d * xps[j + 1]

    return numerator / (1 + tf.abs(denominator))


def c(x, numerator_weights, denominator_weights, training):
    """
    version c of rational activation function

    f(x) = p(x) / q(x) = (a_0 + a_1 * x + a_2 * x^2 + ... + a_n * x^n) /
                (epsilon + |b_0 + b_1 * x + b_2 * x^2 + ... + b_m * x^m|)

    note: q(x) contains a variable term (epsilon) here, and also a b_0 term

    :param x: input tensor
    :param numerator_weights: vector containing the weights a_0, ... a_n
    :param denominator_weights: vector containing the weights b_0, ... b_m
    :param training: whether the call is in inference mode or training mode
    :return: f(x), i.e. the input tensor with the rational activation function applied to it
    """

    xps = _get_xps(x, denominator_weights, numerator_weights)

    numerator = 0
    for i in range(numerator_weights.shape[0]):
        w_n = numerator_weights[i]
        numerator = numerator + w_n * xps[i]

    denominator = 0
    for j in range(denominator_weights.shape[0]):
        w_d = denominator_weights[j]
        denominator = denominator + w_d * xps[j]

    return numerator / (0.1 + tf.abs(denominator))


def d(x, numerator_weights, denominator_weights, training, random_deviation=0.1):
    """
    version d of rational activation function

    f(x) = p(x) / q(x) = (noised(a_0) + noised(a_1) * x + noised(a_2) * x^2 + ... + noised(a_n) * x^n) /
                   (1 + |noised(b_1) * x + noised(b_2) * x^2 + ... + noised(b_m) * X^m|)

    Noised parameters have uniform noise to be in range [(1-random_deviation)*parameter,(1+random_deviation)*parameter].

    :param x: input tensor
    :param numerator_weights: vector containing the weights a_0, ... a_n
    :param denominator_weights: vector containing the weights b_0, ... b_m
    :param training: whether the call is in inference mode or training mode
    :param: random_deviation: random deviation
    :return: f(x), i.e. the input tensor with the rational activation function applied to it

    """
    # TODO @Ting-Yu implement
    raise NotImplementedError()
