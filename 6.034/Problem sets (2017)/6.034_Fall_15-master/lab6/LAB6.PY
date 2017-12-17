# 6.034 Lab 6 2015: Neural Nets & SVMs

from nn_problems import *
from svm_problems import *
from math import e

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

# Optional problem; change TEST_NN_GRID to True to test locally
TEST_NN_GRID = False
nn_grid = [4,]

# Helper functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x >= threshold:
        return 1
    return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1.0/(1.0 + e**(-steepness*(x-midpoint)))

def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -.5*(desired_output - actual_output)**2

# Forward propagation
def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    finaldic = {}
    sortednet = net.topological_sort()
    for neuron in sortednet:
        neuronval = 0.0
        wiresinneuron = net.get_incoming_wires(neuron)
        for wire in wiresinneuron:
            start = wire.startNode
            if type(start) == int:
                neuronval += wire.weight * start
            elif start in net.inputs:
                neuronval += wire.weight * input_values[start]
            else:
                neuronval += wire.weight * finaldic[start]
        finaldic[neuron] = threshold_fn(neuronval)
    return (finaldic[net.get_output_neuron()],finaldic)

# Backward propagation
def calculate_deltas(net, input_values, desired_output):
    """Computes the update coefficient (delta_B) for each neuron in the
    neural net.  Uses sigmoid function to compute output.  Returns a dictionary
    mapping neuron names to update coefficient (delta_B values)."""
    (output,finaldict) = forward_prop(net, input_values, sigmoid)
    deltaoutput = desired_output - output
    updatecoeff = {}
    sortednet = net.topological_sort()
    neuronnumber = len(sortednet)
    index = neuronnumber - 1
    while index >= 0:
        neuron = sortednet[index]
        index -= 1
        outputneuron = finaldict[neuron]
        if net.is_output_neuron(neuron):
            updatecoeff[neuron] = outputneuron * (1 - outputneuron) * deltaoutput
        else:
            outwires = net.get_outgoing_wires(neuron)
            s = 0
            for i in outwires:
                s += i.weight * updatecoeff[i.endNode]
            updatecoeff[neuron] = outputneuron * (1 - outputneuron) * s
    return updatecoeff

def update_weights(net, input_values, desired_output, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses
    sigmoid function to compute output.  Returns the modified neural net, with
    updated weights."""
    '''(output,finaldict) = forward_prop(net, input_values, sigmoid)
    deltaoutput = desired_output - output
    updatecoeff = {}
    sortednet = net.topological_sort()
    neuronnumber = len(sortednet)
    index = neuronnumber - 1
    while index >= 0:
        neuron = sortednet[index]
        index -= 1
        outputneuron = finaldict[neuron]
        if net.is_output_neuron(neuron):
            updatecoeff[neuron] = outputneuron * (1 - outputneuron) * deltaoutput
        else:
            outwires = net.get_outgoing_wires(neuron)
            s = 0
            for i in outwires:
                s += i.weight * updatecoeff[i.endNode]
            updatecoeff[neuron] = outputneuron * (1 - outputneuron) * s'''
    updatecoeff = calculate_deltas(net, input_values, desired_output)
    finaldict = forward_prop(net,input_values,sigmoid)[1]
    for neuron in net.topological_sort():
        neuronval = 0.0
        wiresinneuron = net.get_incoming_wires(neuron)
        for wire in wiresinneuron:
            start = wire.startNode
            if type(start) == int:
                wire.weight += updatecoeff[wire.endNode] * start * r
            elif start in net.inputs:
                wire.weight += updatecoeff[wire.endNode] * input_values[start] * r
            else:
                wire.weight += updatecoeff[wire.endNode] * finaldict[start] * r
    return net

def back_prop(net, input_values, desired_output, r=1, accuracy_threshold=-.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses sigmoid
    function to compute output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    it = 0
    while accuracy(desired_output,forward_prop(net,input_values,sigmoid)[0]) < accuracy_threshold:
        it += 1
        net = update_weights(net,input_values,desired_output,r)
    return (net,it)


#### SUPPORT VECTOR MACHINES ###################################################

# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    ans = 0
    for i in range(len(u)):
        ans += u[i] * v[i]
    return ans

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return dot_product(v,v)**.5

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    return dot_product(svm.boundary.w,point.coords)+svm.boundary.b

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's classification
    is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    p = positiveness(svm,point)
    if p > 0:
        return 1
    elif p == 0:
        return 0
    return -1

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2.0/norm(svm.boundary.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    l = set()
    for sv in svm.support_vectors:
        if positiveness(svm,sv) != sv.classification:
            l.add(sv)
    for tp in svm.training_points:
        if -1 < positiveness(svm,tp) <1:
            l.add(tp)
    return l

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    l = set()
    for tp in svm.training_points:
        if tp in svm.support_vectors:
            if tp.alpha <= 0:
                l.add(tp)
        else:
            if tp.alpha != 0:
                l.add(tp)
    return l

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    s = 0
    for tp in svm.training_points:
        s += tp.classification * tp.alpha
    if s != 0:
        return False
    s = 0
    for tp in svm.training_points:
        coeff = tp.classification * tp.alpha
        if s == 0:
            s = scalar_mult(coeff,tp.coords)
        else:
            s = vector_add(s,scalar_mult(coeff,tp.coords))
    if s != svm.boundary.w:
        return False
    return True

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    l = set()
    for tp in svm.training_points:
        if tp.classification != classify(svm,tp):
            l.add(tp)
    return l


#### SURVEY ####################################################################

NAME = "Sze Nga Wong"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = None
