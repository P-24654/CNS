import numpy as np
plain = np.array([[5,7,10],[13,17,7],[0,5,4]])
cipher = np.array([[3,6,0],[14,16,9],[3,17,11]])
key = (np.linalg.det(plain)*np.linalg.inv(plain) @ cipher)%26
print(key)