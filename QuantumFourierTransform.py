import qiskit
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.visualization import plot_histogram
import qiskit_aer
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt
import os
import numpy as np

def quantumFourierTransformCircuit(qc,N,inverse=False):
    if inverse:
        for i in range(0,int(N/2.)):
            qc.swap(i,N-1-i)
        for i in range(N-1,-1,-1):
            qc.barrier()
            for j in range(N-1,i,-1):
                qc.crz(-(2*np.pi)/(2**(j-i+1)),j,i)
            qc.h(i)
    
    else:    
        for i in range(0,N):
            qc.h(i)
            for j in range(i+1,N):
                qc.crz((2*np.pi)/(2**(j-i+1)),j,i)
            qc.barrier()
        for i in range(0,int(N/2.)):
            qc.swap(i,N-1-i)
    
    return qc

#print(QuantumRegister(2,name = 'q'))

def hadamardAll(qc,N):
    for i in range(0,N):
        qc.h(i)
    qc.barrier()
    return qc

def measureAll(qc,N):
    for i in range(0,N):
        qc.measure(i,i)
    return qc

def initState(qc,N):
    for i in range(0,N):
        if i % 2 == 0:
            qc.x(i)
    qc.barrier()
    return qc

def main(N):
    backend_sim_perfect = AerSimulator()
    
    #qc = QuantumCircuit(2*N,2*N)
    qc = QuantumCircuit(N,N)
    
    #qc = initState(qc,N)
    #qc = measureAll(qc,N)
    #job = backend_sim_perfect.run(qc,shots=1024)
    #result = job.result()
    #plot_histogram(result.get_counts())
    #plt.show()
    
    #psi = qiskit.quantum_info.Statevector.from_int(0b101010,2**6)
    #qc = hadamardAll(qc,N)
    qc = quantumFourierTransformCircuit(qc,N)
    #qc = quantumFourierTransformCircuit(qc,N,inverse=True)
    qc = measureAll(qc,N)
    qc.draw('mpl')
    plt.show()
    #psi.evolve(qc)
    
    job = backend_sim_perfect.run(qc,shots=1024)
    result = job.result()
    plot_histogram(result.get_counts())
    plt.show()


#qc = QuantumCircuit(3,2)
#qc.draw('mpl')
#plt.show()

main(7)

#qc = quantumFourierTransformCircuit(6)
#qc.draw('mpl')
#plt.show()
    
#qc = QuantumCircuit(3)
#qc.ccx(0,1,2)
#qc.draw('mpl')
#plt.show()
