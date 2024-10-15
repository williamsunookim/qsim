import numpy as np
import math

class QSim:
    """ Quantum Simulator
    Implements gates like: hadamard, pauli-x, pauli-z, cnot, swap gates and measurement.
     """
    ket0 = np.array([[1], [0]])
    ket1 = np.array([[0], [1]])
    qubits = []

    def __init__(self, n):
        # n qubits in the system
        self.n = n
        self.qubits = [self.ket0 for i in range(n)]

    def hadamard(self, q):
        # Hadamard gate
        H = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])
        self.qubits[q] = np.dot(H, self.qubits[q])
        return self.qubits[q]

    def pauli_x(self, q):
        # Pauli-X gate
        X = np.array([[0, 1], [1, 0]])
        self.qubits[q] = np.dot(X, self.qubits[q])
        return self.qubits[q]

    def pauli_z(self, q):
        # Pauli-Z gate
        Z = np.array([[1, 0], [0, -1]])
        self.qubits[q] = np.dot(Z, self.qubits[q])
        return self.qubits[q]

    def cnot(self, x_bit, y_bit): # x_bit: Control, y_bit: target
        #print(f'self.qubits[y_bit]: {self.qubits[y_bit]}')
        if np.array_equal(self.qubits[x_bit], self.ket1):
            a = self.qubits[y_bit][0,0]
            b = self.qubits[y_bit][1,0]
            # self.qubits[x_bit] is the same as the past result.
            self.qubits[y_bit] = b*self.ket0 + a*self.ket1
        else:
          pass

        #print(f'self.qubits[y_bit]: {self.qubits[y_bit]}')

    def swap_cnot(self, x_bit, y_bit):
        # SWAP gate: use 3 cnot gates
        self.cnot(x_bit, y_bit)
        self.cnot(y_bit, x_bit)
        self.cnot(x_bit, y_bit)
        return self.qubits[x_bit], self.qubits[y_bit]

    def swap(self, x_bit, y_bit):
        # SWAP gate using matrix multiplication
        #SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
        #res = np.dot(SWAP, self.tensor(self.qubits[x_bit], self.qubits[y_bit]))

        # Reshape the result into two separate qubit states
        #self.qubits[x_bit], self.qubits[y_bit] = res[:2].reshape(2, 1), res[2:].reshape(2, 1)

        # Normalize both qubits
        #self.normalize(x_bit)
        #self.normalize(y_bit)
        temp = self.qubits[x_bit]
        self.qubits[x_bit] = self.qubits[y_bit]
        self.qubits[y_bit] = temp

    def normalize(self, q_num):
        norm = np.linalg.norm(self.qubits[q_num])
        if norm != 0:  # Only normalize if the norm is non-zero
            self.qubits[q_num] = self.qubits[q_num] / norm
        return self.qubits[q_num]

    def measure(self, q, shots):
        # Measure the qubit q
        prob = np.abs(self.qubits[q])**2
        result = np.random.choice([0, 1], shots, p=[prob[0][0], prob[1][0]])
        # result as dictionary, key: result, value: count
        returns = {0: 0, 1: 0}
        for r in result:
            returns[r] += 1
        return returns

    def get_state(self, q):
        return self.qubits[q]

    def set_state(self, q, state):
        self.qubits[q] = state
        return self.qubits[q]

    def get_qubits(self):
        return self.qubits

    def set_qubits(self, qubits):
        self.qubits = qubits
        return self.qubits

    def tensor(self, q1, q2):
        return np.kron(q1, q2)

