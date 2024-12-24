import numpy as np

PROJECT_TO_CART = {"hex_x": np.array([[1, -0.5], [0, 1]], dtype = np.float32)}
PROJECT_CART_TO_TOBJECT_COO = np.array([[1, 0], [0, -1]])
PROJECT_CART_TO_LAYER_COO = np.array([[0, -1], [1, 0]])

class KEY:
    empty_square = "e"