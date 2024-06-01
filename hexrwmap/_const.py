import numpy as np

project_to_cart = {"hex_x": np.array([[1, -0.5], [0, 1]], dtype = np.float32)}
project_cart_to_tobject_coo = np.array([[1, 0], [0, -1]])
project_cart_to_layer_coo = np.array([[0, -1], [1, 0]])