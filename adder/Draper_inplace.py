from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdag, S, Tdagger, Sdag
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger
from math import floor, ceil, log2

def quantum_and(a, b, c, ancilla):
    H | c
    CNOT | (b, ancilla)
    CNOT | (c, a)
    CNOT | (c, b)
    CNOT | (a, ancilla)
    Tdag | a
    Tdag | b
    T | c
    T | ancilla
    CNOT | (a, ancilla)
    CNOT | (c, b)
    CNOT | (c, a)
    CNOT | (b, ancilla)
    H | c
    S | c

def quantum_and_dag(a, b, c):
    H | b
    H | c
    Measure | c
    if(int(c) or resource_check == 1):
        CNOT | (a,b)
        X | c
    H | b

def toffoli_gate(a, b, c, ancilla = 0, mode=True):
    if(TD == 1): # 분해 버전 (일반 시뮬레이터 사용 시 / ResourceCounter 사용 시)
        Tdag | a
        Tdag | b
        H | c
        CNOT | (c, a)
        T | a
        CNOT | (b, c)
        CNOT | (b, a)
        T | c
        Tdag | a
        CNOT | (b, c)
        CNOT | (c, a)
        T | a
        Tdag | c
        CNOT | (b, a)
        H | c
    elif (TD == 2):
        if mode:
            quantum_and(a,b,c,ancilla)
        else:
            quantum_and_dag(a,b,c)
    else: # TD == 0, 분해 안된 버전 사용 (클래식 시뮬레이터 사용 시)
        Toffoli | (a, b, c)

def w(n): # for draper
    return n - sum(int(floor(n / (pow(2, i)))) for i in range(1, int(log2(n)) + 1))

def l(n, t): # for draper
    return int(floor(n / (pow(2, t))))

def inDraper(eng,a,b,ancilla1, ancilla2,n):
    length = n-1-w(n-1)-floor(log2(n-1))

    # Init round
    for i in range(n-1):
        toffoli_gate(a[i], b[i], ancilla1[i])
    for i in range(n):
        CNOT | (a[i], b[i])

    # P-round
    #print("P-rounds")
    idx = 0  # ancilla idx
    tmp = 0  # m=1일 때 idx 저장해두기
    and_idx = 0
    for t in range(1, int(log2(n-1))):
        pre = tmp  # (t-1)일 때의 첫번째 자리 저장
        #print("t ========== ",t)
        for m in range(1, l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                toffoli_gate(b[2 * m], b[2 * m + 1], ancilla2[idx])
                #print(2*m,2*m+1,idx)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                toffoli_gate(ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx])
                #print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx)
            if m == 1:
                tmp = idx
            idx += 1
            and_idx += 1

    # G-round
    #print("G-rounds")
    pre = 0  # The number of cumulative p(t-1)
    idx = 0  # ancilla idx
    for t in range(1, int(log2(n-1)) + 1):
        #print("t = ",t)
        for m in range(l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                toffoli_gate(ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], b[2 * m + 1], ancilla1[int(pow(2, t) * (m + 1)) - 1])

                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1,2 * m + 1,int(pow(2, t) * (m + 1)) - 1)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1,idx+2*m,int(pow(2, t) * (m + 1)) - 1)
                toffoli_gate(ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], ancilla2[idx+2*m],ancilla1[int(pow(2, t) * (m + 1)) - 1])
        if t != 1:
            pre = pre + l(n-1, t - 1) - 1
            idx = pre

    # C-round
    #print("C-rounds")
    if int(log2(n-1)) - 1 == int(log2(2 * (n-1)/ 3)): # p(t-1)까지 접근함
        iter = l(n-1, int(log2(n-1)) - 1) - 1 # 마지막 pt의 개수
    else: # p(t)까지 접근함
        iter = 0
    pre = 0  # (t-1)일 때의 첫번째 idx
    tmp_idx = 0
    for t in range(int(log2(2 * (n-1) / 3)), 0, -1):
        for m in range(1, l(((n-1) - pow(2, t - 1)), t) + 1):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                toffoli_gate(ancilla1[int(pow(2, t) * m) - 1], b[2 * m],ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
                #print(int(pow(2, t) * m) - 1,2 * m,int(pow(2, t) * m + pow(2, t - 1)) - 1)
            else:
                if m==1:
                    iter += l(n-1, t - 1) - 1
                    pre = length - 1 - iter
                toffoli_gate(ancilla1[int(pow(2, t) * m) - 1],ancilla2[pre + 2 * m], ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
                #print(int(pow(2, t) * m) - 1,pre + 2 * m,int(pow(2, t) * m + pow(2, t - 1)) - 1)

            tmp_idx += 1

    # P-inverse round
    #print("P-inverse round")
    pre = 0  # (t-1)일 때의 첫번째 idx
    iter = l(n-1, int(log2(n-1)) - 1) - 1  # 마지막 pt의 개수
    iter2 = 0  # for idx
    idx = 0
    and_idx = 0
    for t in reversed(range(1, int(log2(n-1)))):
        for m in range(1, l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                toffoli_gate(b[2 * m], b[2 * m + 1], ancilla2[m - t])
                #print(2*m, 2*m+1, m-t)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m == 1:
                    iter += l(n-1, t - 1) - 1  # p(t-1) last idx
                    pre = length - iter
                    iter2 += (l(n-1, t) - 1)
                    idx = length - iter2
                toffoli_gate(ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx-1+m])
                #print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx-1+m)
            and_idx += 1

    # mid round
    for i in range(1, n):
        CNOT | (ancilla1[i - 1], b[i])
    for i in range(n-1):
        X | b[i]
    for i in range(1, n-1):
        CNOT | (a[i], b[i])

    ### Step 7. Section3 in reverse. (n-1)bit adder ###

    # P-round reverse
    #print("P-round reverse")
    iter = 0
    pre = 0 # (t-1)일 때의 첫번째 자리 저장
    idx = 0  # ancilla idx
    and_idx = 0

    for t in range(1, int(log2(n-1))):
        if t > 1:
            pre = iter
            iter += l(n-1, t - 1) - 1 # ancilla idx. n is right.
            idx = iter
        #print("t ========== ", t)
        for m in range(1, l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                #print(2 * m, 2 * m + 1, idx)
                toffoli_gate(b[2 * m], b[2 * m + 1], ancilla2[idx])
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                #print(pre - 1 + 2 * m, pre - 1 + 2 * m + 1, idx)
                toffoli_gate(ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx])
            idx += 1
            and_idx += 1

    # C-round reverse
    #print("C-inv-rounds")
    pre = 0  # 이전 p(t) 개수
    tmp_idx = 0
    for t in reversed(range(int(log2(2 * (n-1) / 3)), 0, -1)):
        idx = pre # ancilla2 idx
        for m in range(1, l(((n-1) - pow(2, t - 1)), t) + 1):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                #print(int(pow(2, t) * m) - 1, 2 * m, int(pow(2, t) * m + pow(2, t - 1)) - 1)
                toffoli_gate(ancilla1[int(pow(2, t) * m) - 1], b[2 * m],ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
            else:
                #print(int(pow(2, t) * m) - 1, idx - 1 + 2 * m, int(pow(2, t) * m + pow(2, t - 1)) - 1)
                toffoli_gate(ancilla1[int(pow(2, t) * m) - 1],ancilla2[idx-1+ 2 * m], ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
                if m == 1:
                    pre += l(n-1, t-1) -1

            tmp_idx += 1

    # G-round reverse
    #print("G-inv-rounds")
    pre = 0  # (t-1)일 때의 첫번째 idx
    idx_t = int(log2(n-1)) # n-1이 아니라 n일 때의 t의 범위
    iter = 0
    tmp_idx = 0
    for t in reversed(range(1, int(log2(n-1)) + 1)):
        #print("t=",t)
        for m in range(l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1,2 * m + 1,int(pow(2, t) * (m + 1)) - 1)
                toffoli_gate(ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], b[2 * m + 1],ancilla1[int(pow(2, t) * (m + 1)) - 1])

            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m==0:
                    iter += l(n-1, idx_t-1) - 1  # p(t-1) last idx
                    pre = length - iter
                    idx_t -= 1

                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1, pre - 1 + 2 * m + 1, int(pow(2, t) * (m + 1)) - 1)
                toffoli_gate(ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], ancilla2[pre - 1 + 2 * m + 1],ancilla1[int(pow(2, t) * (m + 1)) - 1])
            tmp_idx += 1

    # P-inverse round reverse
    #print("P-inverse round reverse")
    pre = 0  # (t-1)일 때의 첫번째 idx
    idx_t = int(log2(n-1))-1 # n-1이 아니라 n일 때의 t의 범위
    iter = l(n-1, idx_t) - 1
    iter2 = 0  # for idx
    and_idx = 0
    for t in reversed(range(1, int(log2(n-1)))):
        for m in range(1, l(n-1, t)):
            if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                toffoli_gate(b[2 * m], b[2 * m + 1], ancilla2[m - t])
                #print(2*m,2*m+1,m-t)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m == 1:
                    iter += l(n-1, idx_t-1) - 1  # p(t-1) last idx
                    pre = length - iter
                    iter2 += l(n-1, idx_t) - 1
                    idx = length - iter2
                    idx_t -= 1
                toffoli_gate(ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx-1+m])
                #print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx-1+m)
            and_idx += 1

    # real last
    for i in range(1,n-1):
        CNOT | (a[i], b[i])
    and_idx = 0
    for i in range(n-1):
        toffoli_gate(a[i], b[i], ancilla1[i])
    for i in range(n-1):
        X | b[i]

    result = []
    for k in b:
        result.append(k)

    return result

def adder_test(eng, A, B, n):
    a = eng.allocate_qureg(n)
    b = eng.allocate_qureg(n)

    length = n - 1 - w(n - 1) - floor(log2(n - 1))
    ancilla1 = eng.allocate_qureg(n - 1)  # z[1] ~ z[n] 저장
    ancilla2 = eng.allocate_qureg(length)  # 논문에서 X라고 지칭되는 ancilla



    if (resource_check == 0):
        round_constant_XOR(A, a, n)
        round_constant_XOR(B, b, n)

    if (resource_check == 0):
        print('a: ', end='')
        print_vector(a, n)
        print('b: ', end='')
        print_vector(b, n)

    sum = inDraper(eng,a, b, ancilla1, ancilla2, n)
    # sum = outDraper(a,b,n)

    if (resource_check == 0):
        print('Add result : ', end='')
        print_vector(sum, n)


def round_constant_XOR(rc, qubits, n):
    for i in range(n):
        if ((rc >> i) & 1):
            X | qubits[i]

def print_vector(element, length):
    All(Measure) | element
    for k in range(length):
        print(int(element[length-1-k]), end='')

if __name__ == "__main__":
    n = 32
    a = 0b11001110001000001011010001111110
    b = 0b100111010011011111110011001100111

    TD = 1
    resource_check = 1

    #Resource = ClassicalSimulator()
    Resource = ResourceCounter()
    eng = MainEngine(Resource)
    adder_test(eng,a,b,n)
    print(Resource)
    eng.flush()
