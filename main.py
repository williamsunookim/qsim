from flask import Flask, render_template, request, jsonify
import numpy as np
from qsim import QSim  # QSim 클래스가 qsim.py에 있다고 가정합니다.

app = Flask(__name__)

# 전역적으로 사용할 양자 시뮬레이터 인스턴스
simulator = None

def apply_round_to_all_elements(arr):
    if isinstance(arr, list):
        # 배열(리스트)일 경우 재귀적으로 각 요소에 대해 함수를 호출
        return [apply_round_to_all_elements(elem) for elem in arr]
    else:
        # 숫자일 경우 round 함수를 적용
        return round(arr)

@app.route('/')
def index():
    return render_template('index.html')  # 메인 페이지 렌더링

@app.route('/initialize', methods=['POST'])
def initialize():
    global simulator
    data = request.json
    qubit_count = int(data['qubit_count'])
    
    # 시뮬레이터 초기화 (큐비트 수 설정)
    simulator = QSim(qubit_count)
    print(simulator)
    return jsonify({'message': 'Simulator initialized', 'qubit_count': qubit_count})

@app.route('/apply_gate', methods=['POST'])
def apply_gate():
    global simulator
    data = request.json
    gate = data['gate']
    qubit = int(data['qubit'])
    
    if gate == 'hadamard':
        state = simulator.hadamard(qubit)
    elif gate == 'pauli_x':
        state = simulator.pauli_x(qubit)
    elif gate == 'pauli_z':
        state = simulator.pauli_z(qubit)
    elif gate == 'cnot':
        control_qubit = int(data['control_qubit'])
        state = simulator.cnot(control_qubit, qubit)
    elif gate == 'swap':
        target_qubit = int(data['target_qubit'])
        state = simulator.swap(qubit, target_qubit)
    
    # 현재 전체 큐비트 상태 반환
    qubits_state = [simulator.get_state(i).tolist() for i in range(simulator.n)]

    print(jsonify({'qubits_state': qubits_state}))
    return jsonify({'qubits_state': qubits_state})

@app.route('/measure', methods=['POST'])
def measure():
    global simulator
    data = request.json
    qubit = int(data['qubit'])
    shots = int(data['shots'])
    
    result = simulator.measure(qubit, shots)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
