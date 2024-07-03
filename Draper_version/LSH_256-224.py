from math import floor, ceil, log2
from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, S, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control , Dagger
import random
import sys


IV = [0x068608D3, 0x62D8F7A7, 0xD76652AB, 0x4C600A43, 0xBDC40AA8, 0x1ECA0B68, 0xDA1A89BE, 0x3147D354,
	0x707EB4F9, 0xF65B3862, 0x6B0B2ABE, 0x56B8EC0A, 0xCF237286, 0xEE0D1727, 0x33636595, 0x8BB8D05F]

SC = [0x917caf90, 0x6c1b10a2, 0x6f352943, 0xcf778243, 0x2ceb7472, 0x29e96ff2, 0x8a9ba428, 0x2eeb2642,
	0x0e2c4021, 0x872bb30e, 0xa45e6cb2, 0x46f9c612, 0x185fe69e, 0x1359621b, 0x263fccb2, 0x1a116870,
	0x3a6c612f, 0xb2dec195, 0x02cb1f56, 0x40bfd858, 0x784684b6, 0x6cbb7d2e, 0x660c7ed8, 0x2b79d88a,
	0xa6cd9069, 0x91a05747, 0xcdea7558, 0x00983098, 0xbecb3b2e, 0x2838ab9a, 0x728b573e, 0xa55262b5,
	0x745dfa0f, 0x31f79ed8, 0xb85fce25, 0x98c8c898, 0x8a0669ec, 0x60e445c2, 0xfde295b0, 0xf7b5185a,
	0xd2580983, 0x29967709, 0x182df3dd, 0x61916130, 0x90705676, 0x452a0822, 0xe07846ad, 0xaccd7351,
	0x2a618d55, 0xc00d8032, 0x4621d0f5, 0xf2f29191, 0x00c6cd06, 0x6f322a67, 0x58bef48d, 0x7a40c4fd,
	0x8beee27f, 0xcd8db2f2, 0x67f2c63b, 0xe5842383, 0xc793d306, 0xa15c91d6, 0x17b381e5, 0xbb05c277,
	0x7ad1620a, 0x5b40a5bf, 0x5ab901a2, 0x69a7a768, 0x5b66d9cd, 0xfdee6877, 0xcb3566fc, 0xc0c83a32,
	0x4c336c84, 0x9be6651a, 0x13baa3fc, 0x114f0fd1, 0xc240a728, 0xec56e074, 0x009c63c7, 0x89026cf2,
	0x7f9ff0d0, 0x824b7fb5, 0xce5ea00f, 0x605ee0e2, 0x02e7cfea, 0x43375560, 0x9d002ac7, 0x8b6f5f7b,
	0x1f90c14f, 0xcdcb3537, 0x2cfeafdd, 0xbf3fc342, 0xeab7b9ec, 0x7a8cb5a3, 0x9d2af264, 0xfacedb06,
	0xb052106e, 0x99006d04, 0x2bae8d09, 0xff030601, 0xa271a6d6, 0x0742591d, 0xc81d5701, 0xc9a9e200,
	0x02627f1e, 0x996d719d, 0xda3b9634, 0x02090800, 0x14187d78, 0x499b7624, 0xe57458c9, 0x738be2c9,
	0x64e19d20, 0x06df0f36, 0x15d1cb0e, 0x0b110802, 0x2c95f58c, 0xe5119a6d, 0x59cd22ae, 0xff6eac3c,
	0x467ebd84, 0xe5ee453c, 0xe79cd923, 0x1c190a0d, 0xc28b81b8, 0xf6ac0852, 0x26efd107, 0x6e1ae93b,
	0xc53c41ca, 0xd4338221, 0x8475fd0a, 0x35231729, 0x4e0d3a7a, 0xa2b45b48, 0x16c0d82d, 0x890424a9,
	0x017e0c8f, 0x07b5a3f5, 0xfa73078e, 0x583a405e, 0x5b47b4c8, 0x570fa3ea, 0xd7990543, 0x8d28ce32,
	0x7f8a9b90, 0xbd5998fc, 0x6d7a9688, 0x927a9eb6, 0xa2fc7d23, 0x66b38e41, 0x709e491a, 0xb5f700bf,
	0x0a262c0f, 0x16f295b9, 0xe8111ef5, 0x0d195548, 0x9f79a0c5, 0x1a41cfa7, 0x0ee7638a, 0xacf7c074,
	0x30523b19, 0x09884ecf, 0xf93014dd, 0x266e9d55, 0x191a6664, 0x5c1176c1, 0xf64aed98, 0xa4b83520,
	0x828d5449, 0x91d71dd8, 0x2944f2d6, 0x950bf27b, 0x3380ca7d, 0x6d88381d, 0x4138868e, 0x5ced55c4,
	0x0fe19dcb, 0x68f4f669, 0x6e37c8ff, 0xa0fe6e10, 0xb44b47b0, 0xf5c0558a, 0x79bf14cf, 0x4a431a20,
	0xf17f68da, 0x5deb5fd1, 0xa600c86d, 0x9f6c7eb0, 0xff92f864, 0xb615e07f, 0x38d3e448, 0x8d5d3a6a,
	0x70e843cb, 0x494b312e, 0xa6c93613, 0x0beb2f4f, 0x928b5d63, 0xcbf66035, 0x0cb82c80, 0xea97a4f7,
	0x592c0f3b, 0x947c5f77, 0x6fff49b9, 0xf71a7e5a, 0x1de8c0f5, 0xc2569600, 0xc4e4ac8c, 0x823c9ce1]

gamma = [0, 8, 16, 24, 24, 16, 8, 0]

def main(eng):
    n=32
    msg_e_l = eng.allocate_qureg(256)
    msg_e_r = eng.allocate_qureg(256)
    msg_o_l = eng.allocate_qureg(256)
    msg_o_r = eng.allocate_qureg(256)
    cv_l = eng.allocate_qureg(256)
    cv_r = eng.allocate_qureg(256)
    ancilla = []
    ancilla2 = []
    ancilla_exp = []
    ancilla_exp2 = []
    length = n - 1 - w(n - 1) - floor(log2(n - 1))
    # ancilla = eng.allocate_qureg(16)
    # ancilla2 = eng.allocate_qureg(16)

    for i in range(16):
        ancilla.append(eng.allocate_qureg(n-1))
        ancilla2.append(eng.allocate_qureg(length))
        ancilla_exp.append(eng.allocate_qureg(n - 1))
        ancilla_exp2.append(eng.allocate_qureg(length))

    init(eng,cv_l,cv_r)

    if(resource_check!=1):
        Round_constant_XOR(eng,msg_e_l, 0x0000000053662F21243B6688D2EDF1D8A3E069D78FE69993CCBEA6F99CCC7FB6,256)
        Round_constant_XOR(eng,msg_e_r, 0x0000000000000000000000000000000000000000000000000000000000000000,256)

    # if (resource_check != 1):
    #     Round_constant_XOR(eng, msg_e_l, 0x5cba6cd0d8bb8f9566b10d74a0a45eaa6c81ad3a196815d4bc381c06cb5a6ea8, 256)
    #     Round_constant_XOR(eng, msg_e_r, 0x0000000000000000000000000000000000000000000000000000000000000080, 256)

    X | msg_e_l[231]

    # if (resource_check != 1):
    #     print_state(eng,msg_e_l,64)


    cv_l, cv_r = compress(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,cv_l,cv_r,ancilla,ancilla2,ancilla_exp,ancilla_exp2)
    final(eng,cv_l,cv_r)

    if (resource_check != 1):
        print_state(eng, cv_l[0:224], 56)

    if (resource_check != 1):
        print_state(eng, cv_l, 64)
        print_state(eng, cv_l[0:32], 8)
        print_state(eng, cv_l[32:64], 8)
        print_state(eng, cv_l[64:96], 8)
        print_state(eng, cv_l[96:128], 8)
        print_state(eng, cv_l[128:160], 8)
        print_state(eng, cv_l[160:192], 8)
        print_state(eng, cv_l[192:224], 8)
        print_state(eng, cv_l[224:256], 8)


def init(eng,cv_l,cv_r):

    #cv_l[0] -> cv_l[0:32]

    for i in range(8):
        Round_constant_XOR(eng,cv_l[32*i:32*(i+1)],IV[i],32)
        Round_constant_XOR(eng,cv_r[32*i:32*(i+1)],IV[8+i],32)

def compress(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,cv_l,cv_r,ancilla,ancilla2,ancilla_exp,ancilla_exp2):
    msg_add(eng,msg_e_l,msg_e_r,cv_l,cv_r)

    # if (resource_check != 1):
    #     print_state(eng, cv_l, 64)
    #     print_state(eng, cv_l[0:32], 8)
    #     print_state(eng, cv_l[32:64], 8)
    #     print_state(eng, cv_l[64:96], 8)
    #     print_state(eng, cv_l[96:128], 8)
    #     print_state(eng, cv_l[128:160], 8)
    #     print_state(eng, cv_l[160:192], 8)
    #     print_state(eng, cv_l[192:224], 8)
    #     print_state(eng, cv_l[224:256], 8)
    #
    # if (resource_check != 1):
    #     print_state(eng, cv_r, 64)
    #     print_state(eng, cv_r[0:32], 8)
    #     print_state(eng, cv_r[32:64], 8)
    #     print_state(eng, cv_r[64:96], 8)
    #     print_state(eng, cv_r[96:128], 8)
    #     print_state(eng, cv_r[128:160], 8)
    #     print_state(eng, cv_r[160:192], 8)
    #     print_state(eng, cv_r[192:224], 8)
    #     print_state(eng, cv_r[224:256], 8)

    mix(eng,cv_l,cv_r,29,1,ancilla,ancilla2,0)
    cv_l, cv_r = word_perm(eng,cv_l,cv_r)

    #
    msg_add(eng,msg_o_l,msg_o_r,cv_l,cv_r)
    mix(eng, cv_l, cv_r, 5, 17, ancilla,ancilla2,8)
    cv_l, cv_r = word_perm(eng,cv_l,cv_r)

    for i in range(1,13):
        msg_e_l, msg_e_r= msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla_exp,ancilla_exp2)
        msg_add(eng,msg_e_l,msg_e_r,cv_l,cv_r)
        mix(eng,cv_l,cv_r,29,1,ancilla,ancilla2,16 * i)
        cv_l, cv_r = word_perm(eng, cv_l, cv_r)

        msg_o_l, msg_o_r = msg_exp_odd(eng, msg_e_l, msg_e_r, msg_o_l, msg_o_r, ancilla_exp,ancilla_exp2)
        msg_add(eng, msg_o_l, msg_o_r, cv_l, cv_r)
        mix(eng, cv_l, cv_r, 5, 17, ancilla,ancilla2, 16 * i + 8)
        cv_l, cv_r = word_perm(eng, cv_l, cv_r)

    msg_e_l, msg_e_r= msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla_exp,ancilla_exp2)
    msg_add(eng, msg_e_l, msg_e_r, cv_l, cv_r)

    return cv_l, cv_r

def final(eng,cv_l,cv_r):
    for i in range(8):
        CNOT32(eng, cv_r[32 * i:32 * (i + 1)], cv_l[32 * i:32 * (i + 1)])

    # if (resource_check != 1):
    #     print_state(eng, cv_l, 64)
    #     print_state(eng, cv_l[0:32], 8)
    #     print_state(eng, cv_l[32:64], 8)
    #     print_state(eng, cv_l[64:96], 8)
    #     print_state(eng, cv_l[96:128], 8)
    #     print_state(eng, cv_l[128:160], 8)
    #     print_state(eng, cv_l[160:192], 8)
    #     print_state(eng, cv_l[192:224], 8)
    #     print_state(eng, cv_l[224:256], 8)
    #
    # print("------------------------------------")
def msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla,ancilla2):
    msg_e_l = msg_perm(eng,msg_e_l)
    msg_e_r = msg_perm(eng, msg_e_r)

    for i in range(8):
        msg_e_l[32*i:32*(i+1)] = inDraper(eng,msg_o_l[32 * i :32 * (i + 1)],msg_e_l[32*i:32*(i+1)],ancilla[i],ancilla2[i],32)
        msg_e_r[32 * i:32 * (i + 1)] =inDraper(eng, msg_o_r[32 * i:32 * (i + 1)], msg_e_r[32 * i:32 * (i + 1)], ancilla[i+8], ancilla2[i+8],32)
        # CDKM(eng,msg_o_l[32 * i :32 * (i + 1)],msg_e_l[32*i:32*(i+1)],ancilla[i],32)
        # CDKM(eng, msg_o_r[32 * i:32 * (i + 1)], msg_e_r[32 * i:32 * (i + 1)], ancilla[i+8], 32)

    return msg_e_l, msg_e_r

def msg_exp_odd(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla,ancilla2):
    msg_o_l = msg_perm(eng,msg_o_l)
    msg_o_r = msg_perm(eng, msg_o_r)

    for i in range(8):
        msg_o_l[32 * i:32 * (i + 1)] = inDraper(eng, msg_e_l[32 * i:32 * (i + 1)], msg_o_l[32 * i:32 * (i + 1)],
                                                ancilla[i], ancilla2[i], 32)
        msg_o_r[32 * i:32 * (i + 1)] = inDraper(eng, msg_e_r[32 * i:32 * (i + 1)], msg_o_r[32 * i:32 * (i + 1)],
                                                ancilla[i + 8], ancilla2[i + 8], 32)
        # CDKM(eng, msg_e_l[32 * i:32 * (i + 1)], msg_o_l[32 * i:32 * (i + 1)], ancilla[i], 32)
        # CDKM(eng, msg_e_r[32 * i:32 * (i + 1)], msg_o_r[32 * i:32 * (i + 1)], ancilla[i+8], 32)

    return msg_o_l, msg_o_r

def msg_perm(eng,msg): #3,2,0,1,7,4,5,6
    new_msg = []
    append(eng, new_msg, msg, 3)
    append(eng, new_msg, msg, 2)
    append(eng, new_msg, msg, 0)
    append(eng, new_msg, msg, 1)
    append(eng, new_msg, msg, 7)
    append(eng, new_msg, msg, 4)
    append(eng, new_msg, msg, 5)
    append(eng, new_msg, msg, 6)

    return new_msg


def append(eng,new_msg,msg,count):
    for i in range(32):
        new_msg.append(msg[32*count +i])


def msg_add(eng,msg_l,msg_r,cv_l,cv_r):

    for i in range(8):
        CNOT32(eng, msg_l[32*i:32*(i+1)], cv_l[32*i:32*(i+1)])
        CNOT32(eng, msg_r[32 * i:32 * (i + 1)], cv_r[32 * i:32 * (i + 1)])


def mix(eng,cv_l,cv_r,alpha,beta,ancilla,ancilla2,sc_count):
    for i in range(8):
        #CDKM(eng,cv_r[32 * i : 32 * (i + 1)], cv_l[32 * i : 32 * (i + 1)], ancilla[i],32)
        cv_l[32 * i : 32 * (i + 1)] = inDraper(eng,cv_r[32 * i : 32 * (i + 1)], cv_l[32 * i : 32 * (i + 1)],ancilla[i],ancilla2[i],32)

    #rotation a
    for i in range(8):
        cv_l[32 * i : 32 * (i + 1)] = rotation(eng,cv_l[32 * i: 32 * (i + 1)],alpha)

    # xor with SC
    for i in range(8):
        Round_constant_XOR(eng,cv_l[32 * i : 32 * (i + 1)],SC[i+sc_count],32) # modify

    for i in range(8):
        #CDKM(eng,cv_l[32 * i : 32 * (i + 1)], cv_r[32 * i : 32 * (i + 1)], ancilla[i],32)
        cv_r[32 * i : 32 * (i + 1)] = inDraper(eng, cv_l[32 * i : 32 * (i + 1)], cv_r[32 * i : 32 * (i + 1)], ancilla[i], ancilla2[i], 32)

    # rotation B
    for i in range(8):
        cv_r[32 * i: 32 * (i + 1)] = rotation(eng, cv_r[32 * i: 32 * (i + 1)], beta)
    #

    for i in range(8):
        #CDKM(eng,cv_r[32 * i : 32 * (i + 1)], cv_l[32 * i : 32 * (i + 1)], ancilla[i],32)
        cv_l[32 * i: 32 * (i + 1)] = inDraper(eng, cv_r[32 * i: 32 * (i + 1)], cv_l[32 * i: 32 * (i + 1)], ancilla[i], ancilla2[i], 32)
    #
    # rotation gamma
    for i in range(1,7):
        cv_r[32 * i : 32 * (i + 1)] = rotation(eng,cv_r[32 * i : 32 * (i + 1)],gamma[i])

    # if (resource_check != 1):
    #     print_state(eng, cv_r, 64)
    #     print_state(eng, cv_r[0:32], 8)
    #     print_state(eng, cv_r[32:64], 8)
    #     print_state(eng, cv_r[64:96], 8)
    #     print_state(eng, cv_r[96:128], 8)
    #     print_state(eng, cv_r[128:160], 8)
    #     print_state(eng, cv_r[160:192], 8)
    #     print_state(eng, cv_r[192:224], 8)
    #     print_state(eng, cv_r[224:256], 8)

def rotation(eng,cv,constant):
    new_cv =[]
    for i in range(32-constant,32):
        new_cv.append(cv[i])
    for i in range(32-constant):
        new_cv.append(cv[i])

    return new_cv

def word_perm(eng,cv_l,cv_r):
    new_cv_l =[]
    new_cv_r = []

    append(eng, new_cv_l,cv_l,6)
    append(eng, new_cv_l, cv_l, 4)
    append(eng, new_cv_l, cv_l, 5)
    append(eng, new_cv_l, cv_l, 7)
    append(eng, new_cv_l, cv_r, 4)
    append(eng, new_cv_l, cv_r, 7)
    append(eng, new_cv_l, cv_r, 6)
    append(eng, new_cv_l, cv_r, 5)

    append(eng, new_cv_r, cv_l, 2)
    append(eng, new_cv_r, cv_l, 0)
    append(eng, new_cv_r, cv_l, 1)
    append(eng, new_cv_r, cv_l, 3)
    append(eng, new_cv_r, cv_r, 0)
    append(eng, new_cv_r, cv_r, 3)
    append(eng, new_cv_r, cv_r, 2)
    append(eng, new_cv_r, cv_r, 1)

    return new_cv_l, new_cv_r


def CNOT32(eng,a,b):
    for i in range(32):
        CNOT | (a[i], b[i])



# def CDKM(eng, a, b, c, n):
#     for i in range(n - 2):
#         CNOT | (a[i + 1], b[i + 1])
#
#     CNOT | (a[1], c)
#     Toffoli_gate(eng, a[0], b[0], c)
#     CNOT | (a[2], a[1])
#     Toffoli_gate(eng, c, b[1], a[1])
#     CNOT | (a[3], a[2])
#
#     for i in range(n - 5):
#         Toffoli_gate(eng, a[i + 1], b[i + 2], a[i + 2])
#         CNOT | (a[i + 4], a[i + 3])
#
#     Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
#     CNOT | (a[n - 2], b[n - 1])
#     CNOT | (a[n - 1], b[n - 1])
#     Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])
#
#     for i in range(n - 3):
#         X | b[i + 1]
#
#     CNOT | (c, b[1])
#
#     for i in range(n - 3):
#         CNOT | (a[i + 1], b[i + 2])
#
#     Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
#
#     for i in range(n - 5):
#         Toffoli_gate(eng, a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
#         CNOT | (a[n - 2 - i], a[n - 3 - i])
#         X | (b[n - 3 - i])
#
#     Toffoli_gate(eng, c, b[1], a[1])
#     CNOT | (a[3], a[2])
#     X | b[2]
#     Toffoli_gate(eng, a[0], b[0], c)
#     CNOT | (a[2], a[1])
#     X | b[1]
#     CNOT | (a[1], c)
#
#     for i in range(n-1):
#         CNOT | (a[i], b[i])

def w(n): # for draper
    return n - sum(int(floor(n / (pow(2, i)))) for i in range(1, int(log2(n)) + 1))

def l(n, t): # for draper
    return int(floor(n / (pow(2, t))))

def inDraper(eng,a,b,ancilla1, ancilla2,n):
    length = n-1-w(n-1)-floor(log2(n-1))

    # Init round
    for i in range(n-1):
        toffoli_gate(eng,a[i], b[i], ancilla1[i])
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
                toffoli_gate(eng,b[2 * m], b[2 * m + 1], ancilla2[idx])
                #print(2*m,2*m+1,idx)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                toffoli_gate(eng,ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx])
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
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], b[2 * m + 1], ancilla1[int(pow(2, t) * (m + 1)) - 1])

                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1,2 * m + 1,int(pow(2, t) * (m + 1)) - 1)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1,idx+2*m,int(pow(2, t) * (m + 1)) - 1)
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], ancilla2[idx+2*m],ancilla1[int(pow(2, t) * (m + 1)) - 1])
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
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m) - 1], b[2 * m],ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
                #print(int(pow(2, t) * m) - 1,2 * m,int(pow(2, t) * m + pow(2, t - 1)) - 1)
            else:
                if m==1:
                    iter += l(n-1, t - 1) - 1
                    pre = length - 1 - iter
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m) - 1],ancilla2[pre + 2 * m], ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
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
                toffoli_gate(eng,b[2 * m], b[2 * m + 1], ancilla2[m - t])
                #print(2*m, 2*m+1, m-t)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m == 1:
                    iter += l(n-1, t - 1) - 1  # p(t-1) last idx
                    pre = length - iter
                    iter2 += (l(n-1, t) - 1)
                    idx = length - iter2
                toffoli_gate(eng,ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx-1+m])
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
                toffoli_gate(eng,b[2 * m], b[2 * m + 1], ancilla2[idx])
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                #print(pre - 1 + 2 * m, pre - 1 + 2 * m + 1, idx)
                toffoli_gate(eng,ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx])
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
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m) - 1], b[2 * m],ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
            else:
                #print(int(pow(2, t) * m) - 1, idx - 1 + 2 * m, int(pow(2, t) * m + pow(2, t - 1)) - 1)
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m) - 1],ancilla2[idx-1+ 2 * m], ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1])
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
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], b[2 * m + 1],ancilla1[int(pow(2, t) * (m + 1)) - 1])

            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m==0:
                    iter += l(n-1, idx_t-1) - 1  # p(t-1) last idx
                    pre = length - iter
                    idx_t -= 1

                #print(int(pow(2, t) * m + pow(2, t - 1)) - 1, pre - 1 + 2 * m + 1, int(pow(2, t) * (m + 1)) - 1)
                toffoli_gate(eng,ancilla1[int(pow(2, t) * m + pow(2, t - 1)) - 1], ancilla2[pre - 1 + 2 * m + 1],ancilla1[int(pow(2, t) * (m + 1)) - 1])
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
                toffoli_gate(eng,b[2 * m], b[2 * m + 1], ancilla2[m - t])
                #print(2*m,2*m+1,m-t)
            else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                if m == 1:
                    iter += l(n-1, idx_t-1) - 1  # p(t-1) last idx
                    pre = length - iter
                    iter2 += l(n-1, idx_t) - 1
                    idx = length - iter2
                    idx_t -= 1
                toffoli_gate(eng,ancilla2[pre - 1 + 2 * m], ancilla2[pre - 1 + 2 * m + 1], ancilla2[idx-1+m])
                #print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx-1+m)
            and_idx += 1

    # real last
    for i in range(1,n-1):
        CNOT | (a[i], b[i])
    and_idx = 0
    for i in range(n-1):
        toffoli_gate(eng,a[i], b[i], ancilla1[i])
    for i in range(n-1):
        X | b[i]

    result = []
    for k in b:
        result.append(k)

    return result

def print_state(eng, b, len): # if b is 128-bit -> len is 32

    All(Measure) | b
    print('0x', end='')
    print_hex(eng, b, len)
    print('\n')

def print_binary(eng, b, n):   # binary
    All(Measure) | b
    print('Result : ', end='')
    for i in range(n):
        print(int(b[n - 1 - i]), end='')
    print('\n')

def print_hex(eng, qubits, len):

    for i in reversed(range(len)):
        temp = 0
        temp = temp + int(qubits[4 * i + 3]) * 8
        temp = temp + int(qubits[4 * i + 2]) * 4
        temp = temp + int(qubits[4 * i + 1]) * 2
        temp = temp + int(qubits[4 * i])

        temp = hex(temp)
        y = temp.replace("0x", "")
        print(y, end='')

def toffoli_gate(eng, a, b, c):
    #Toffoli | (a, b, c)

    if (resource_check):
        if (AND_check):
            ancilla = eng.allocate_qubit()
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

        else:
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
    else:
        Toffoli | (a, b, c)

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]
    # print_state(eng,k,bit)


global resource_check
global AND_check
global count
count =0
# print('Generate Ciphertext…')
# Simulate = ClassicalSimulator()
# eng = MainEngine(Simulate)
# resource_check = 0
# main(eng)
# eng.flush()

print('Estimate cost…')
Resource = ResourceCounter()
eng = MainEngine(Resource)
resource_check = 1
AND_check = 0
main(eng)
print(Resource)
# print(count)
# print('\n')
eng.flush()