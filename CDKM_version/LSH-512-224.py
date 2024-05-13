import math
from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, T, Tdag, S, Swap
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control , Dagger
import random
import sys

IV = [0x0C401E9FE8813A55, 0x4A5F446268FD3D35, 0xFF13E452334F612A, 0xF8227661037E354A,
	0xA5F223723C9CA29D, 0x95D965A11AED3979, 0x01E23835B9AB02CC, 0x52D49CBAD5B30616,
	0x9E5C2027773F4ED3, 0x66A5C8801925B701, 0x22BBC85B4C6779D9, 0xC13171A42C559C23,
	0x31E2B67D25BE3813, 0xD522C4DEED8E4D83, 0xA79F5509B43FBAFE, 0xE00D2CD88B4B6C6A,]

SC = [0x97884283c938982a, 0xba1fca93533e2355, 0xc519a2e87aeb1c03, 0x9a0fc95462af17b1,
	0xfc3dda8ab019a82b, 0x02825d079a895407, 0x79f2d0a7ee06a6f7, 0xd76d15eed9fdf5fe,
	0x1fcac64d01d0c2c1, 0xd9ea5de69161790f, 0xdebc8b6366071fc8, 0xa9d91db711c6c94b,
	0x3a18653ac9c1d427, 0x84df64a223dd5b09, 0x6cc37895f4ad9e70, 0x448304c8d7f3f4d5,
	0xea91134ed29383e0, 0xc4484477f2da88e8, 0x9b47eec96d26e8a6, 0x82f6d4c8d89014f4,
	0x527da0048b95fb61, 0x644406c60138648d, 0x303c0e8aa24c0edc, 0xc787cda0cbe8ca19,
	0x7ba46221661764ca, 0x0c8cbc6acd6371ac, 0xe336b836940f8f41, 0x79cb9da168a50976,
	0xd01da49021915cb3, 0xa84accc7399cf1f1, 0x6c4a992cee5aeb0c, 0x4f556e6cb4b2e3e0,
	0x200683877d7c2f45, 0x9949273830d51db8, 0x19eeeecaa39ed124, 0x45693f0a0dae7fef,
	0xedc234b1b2ee1083, 0xf3179400d68ee399, 0xb6e3c61b4945f778, 0xa4c3db216796c42f,
	0x268a0b04f9ab7465, 0xe2705f6905f2d651, 0x08ddb96e426ff53d, 0xaea84917bc2e6f34,
	0xaff6e664a0fe9470, 0x0aab94d765727d8c, 0x9aa9e1648f3d702e, 0x689efc88fe5af3d3,
	0xb0950ffea51fd98b, 0x52cfc86ef8c92833, 0xe69727b0b2653245, 0x56f160d3ea9da3e2,
	0xa6dd4b059f93051f, 0xb6406c3cd7f00996, 0x448b45f3ccad9ec8, 0x079b8587594ec73b,
	0x45a50ea3c4f9653b, 0x22983767c1f15b85, 0x7dbed8631797782b, 0x485234be88418638,
	0x842850a5329824c5, 0xf6aca914c7f9a04c, 0xcfd139c07a4c670c, 0xa3210ce0a8160242,
	0xeab3b268be5ea080, 0xbacf9f29b34ce0a7, 0x3c973b7aaf0fa3a8, 0x9a86f346c9c7be80,
	0xac78f5d7cabcea49, 0xa355bddcc199ed42, 0xa10afa3ac6b373db, 0xc42ded88be1844e5,
	0x9e661b271cff216a, 0x8a6ec8dd002d8861, 0xd3d2b629beb34be4, 0x217a3a1091863f1a,
	0x256ecda287a733f5, 0xf9139a9e5b872fe5, 0xac0535017a274f7c, 0xf21b7646d65d2aa9,
	0x048142441c208c08, 0xf937a5dd2db5e9eb, 0xa688dfe871ff30b7, 0x9bb44aa217c5593b,
	0x943c702a2edb291a, 0x0cae38f9e2b715de, 0xb13a367ba176cc28, 0x0d91bd1d3387d49b,
	0x85c386603cac940c, 0x30dd830ae39fd5e4, 0x2f68c85a712fe85d, 0x4ffeecb9dd1e94d6,
	0xd0ac9a590a0443ae, 0xbae732dc99ccf3ea, 0xeb70b21d1842f4d9, 0x9f4eda50bb5c6fa8,
	0x4949e69ce940a091, 0x0e608dee8375ba14, 0x983122cba118458c, 0x4eeba696fbb36b25,
	0x7d46f3630e47f27e, 0xa21a0f7666c0dea4, 0x5c22cf355b37cec4, 0xee292b0c17cc1847,
	0x9330838629e131da, 0x6eee7c71f92fce22, 0xc953ee6cb95dd224, 0x3a923d92af1e9073,
	0xc43a5671563a70fb, 0xbc2985dd279f8346, 0x7ef2049093069320, 0x17543723e3e46035,
	0xc3b409b00b130c6d, 0x5d6aee6b28fdf090, 0x1d425b26172ff6ed, 0xcccfd041cdaf03ad,
	0xfe90c7c790ab6cbf, 0xe5af6304c722ca02, 0x70f695239999b39e, 0x6b8b5b07c844954c,
	0x77bdb9bb1e1f7a30, 0xc859599426ee80ed, 0x5f9d813d4726e40a, 0x9ca0120f7cb2b179,
	0x8f588f583c182cbd, 0x951267cbe9eccce7, 0x678bb8bd334d520e, 0xf6e662d00cd9e1b7,
	0x357774d93d99aaa7, 0x21b2edbb156f6eb5, 0xfd1ebe846e0aee69, 0x3cb2218c2f642b15,
	0xe7e7e7945444ea4c, 0xa77a33b5d6b9b47c, 0xf34475f0809f6075, 0xdd4932dce6bb99ad,
	0xacec4e16d74451dc, 0xd4a0a8d084de23d6, 0x1bdd42f278f95866, 0xeed3adbb938f4051,
	0xcfcf7be8992f3733, 0x21ade98c906e3123, 0x37ba66711fffd668, 0x267c0fc3a255478a,
	0x993a64ee1b962e88, 0x754979556301faaa, 0xf920356b7251be81, 0xc281694f22cf923f,
	0x9f4b6481c8666b02, 0xcf97761cfe9f5444, 0xf220d7911fd63e9f, 0xa28bd365f79cd1b0,
	0xd39f5309b1c4b721, 0xbec2ceb864fca51f, 0x1955a0ddc410407a, 0x43eab871f261d201,
	0xeaafe64a2ed16da1, 0x670d931b9df39913, 0x12f868b0f614de91, 0x2e5f395d946e8252,
	0x72f25cbb767bd8f4, 0x8191871d61a1c4dd, 0x6ef67ea1d450ba93, 0x2ea32a645433d344,
	0x9a963079003f0f8b, 0x74a0aeb9918cac7a, 0x0b6119a70af36fa3, 0x8d9896f202f0d480,
	0x654f1831f254cd66, 0x1318a47f0366a25e, 0x65752076250b4e01, 0xd1cd8eb888071772,
	0x30c6a9793f4e9b25, 0x154f684b1e3926ee, 0x6c7ac0b1fe6312ae, 0x262f88f4f3c5550d,
	0xb4674a24472233cb, 0x2bbd23826a090071, 0xda95969b30594f66, 0x9f5c47408f1e8a43,
	0xf77022b88de9c055, 0x64b7b36957601503, 0xe73b72b06175c11a, 0x55b87de8b91a6233,
	0x1bb16e6b6955ff7f, 0xe8e0a5ec7309719c, 0x702c31cb89a8b640, 0xfba387cfada8cde2,
	0x6792db4677aa164c, 0x1c6b1cc0b7751867, 0x22ae2311d736dc01, 0x0e3666a1d37c9588,
	0xcd1fd9d4bf557e9a, 0xc986925f7c7b0e84, 0x9c5dfd55325ef6b0, 0x9f2b577d5676b0dd,
	0xfa6e21be21c062b3, 0x8787dd782c8d7f83, 0xd0d134e90e12dd23, 0x449d087550121d96,
	0xecf9ae9414d41967, 0x5018f1dbf789934d, 0xfa5b52879155a74c, 0xca82d4d3cd278e7c,
	0x688fdfdfe22316ad, 0x0f6555a4ba0d030a, 0xa2061df720f000f3, 0xe1a57dc5622fb3da,
	0xe6a842a8e8ed8153, 0x690acdd3811ce09d, 0x55adda18e6fcf446, 0x4d57a8a0f4b60b46,
	0xf86fbfc20539c415, 0x74bafa5ec7100d19, 0xa824151810f0f495, 0x8723432791e38ebb,
	0x8eeaeb91d66ed539, 0x73d8a1549dfd7e06, 0x0387f2ffe3f13a9b, 0xa5004995aac15193,
	0x682f81c73efdda0d, 0x2fb55925d71d268d, 0xcc392d2901e58a3d, 0xaa666ab975724a42]

gamma = [0, 16, 32, 48, 8, 24, 40, 56]

def main(eng):
    msg_e_l = eng.allocate_qureg(512)
    msg_e_r = eng.allocate_qureg(512)
    msg_o_l = eng.allocate_qureg(512)
    msg_o_r = eng.allocate_qureg(512)
    cv_l = eng.allocate_qureg(512)
    cv_r = eng.allocate_qureg(512)
    ancilla = eng.allocate_qureg(16)
    ancilla2 = eng.allocate_qureg(16)
    init(eng,cv_l,cv_r)

    if(resource_check!=1):
        Round_constant_XOR(eng,msg_e_l, 0x0000000000000000000000000000000000000000000000000000000000000000000000000B8578D93F64BB374714CB6790D73A1D04198868C1E104C01D76E44C,512)
        #Round_constant_XOR(eng,msg_e_r, 0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,512)

    X | msg_e_l[231]

    # if (resource_check != 1):
    #     print_state(eng, msg_e_l, 128)
    #     print_state(eng, msg_e_l[0:64], 16)
    #     print_state(eng, msg_e_l[64:128], 16)
    #     print_state(eng, msg_e_l[128:192], 16)
    #     print_state(eng, msg_e_l[192:256], 16)
    #     print_state(eng, msg_e_l[256:320], 16)
    #     print_state(eng, msg_e_l[320:384], 16)
    #     print_state(eng, msg_e_l[384:448], 16)
    #     print_state(eng, msg_e_l[448:512], 16)
    #
    #     print_state(eng, msg_e_r, 128)
    #     print_state(eng, msg_e_r[0:64], 16)
    #     print_state(eng, msg_e_r[64:128], 16)
    #     print_state(eng, msg_e_r[128:192], 16)
    #     print_state(eng, msg_e_r[192:256], 16)
    #     print_state(eng, msg_e_r[256:320], 16)
    #     print_state(eng, msg_e_r[320:384], 16)
    #     print_state(eng, msg_e_r[384:448], 16)
    #     print_state(eng, msg_e_r[448:512], 16)

    cv_l, cv_r = compress(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,cv_l,cv_r,ancilla,ancilla2)
    final(eng,cv_l,cv_r)

    if (resource_check != 1):
        print_state(eng, cv_l, 128)
        print_state(eng, cv_l[0:64], 16)
        print_state(eng, cv_l[64:128], 16)
        print_state(eng, cv_l[128:192], 16)
        print_state(eng, cv_l[192:256], 16)
        print_state(eng, cv_l[256:320], 16)
        print_state(eng, cv_l[320:384], 16)
        print_state(eng, cv_l[384:448], 16)
        print_state(eng, cv_l[448:512], 16)


def init(eng,cv_l,cv_r):

    #cv_l[0] -> cv_l[0:32]

    for i in range(8):
        Round_constant_XOR(eng,cv_l[64*i:64*(i+1)],IV[i],64)
        Round_constant_XOR(eng,cv_r[64*i:64*(i+1)],IV[8+i],64)

def compress(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,cv_l,cv_r,ancilla,ancilla2):
    msg_add(eng,msg_e_l,msg_e_r,cv_l,cv_r)
    mix(eng,cv_l,cv_r,23,59,ancilla,0)
    cv_l, cv_r = word_perm(eng,cv_l,cv_r)

    # if (resource_check != 1):
    #     print_state(eng, cv_l, 128)
    #     print_state(eng, cv_l[0:64], 16)
    #     print_state(eng, cv_l[64:128], 16)
    #     print_state(eng, cv_l[128:192], 16)
    #     print_state(eng, cv_l[192:256], 16)
    #     print_state(eng, cv_l[256:320], 16)
    #     print_state(eng, cv_l[320:384], 16)
    #     print_state(eng, cv_l[384:448], 16)
    #     print_state(eng, cv_l[448:512], 16)
    #
    #     print("------------------------------------")
    #
    # if (resource_check != 1):
    #     print_state(eng, cv_r, 128)
    #     print_state(eng, cv_r[0:64], 16)
    #     print_state(eng, cv_r[64:128], 16)
    #     print_state(eng, cv_r[128:192], 16)
    #     print_state(eng, cv_r[192:256], 16)
    #     print_state(eng, cv_r[256:320], 16)
    #     print_state(eng, cv_r[320:384], 16)
    #     print_state(eng, cv_r[384:448], 16)
    #     print_state(eng, cv_r[448:512], 16)
    #
    #     print("------------------------------------")

    #
    msg_add(eng,msg_o_l,msg_o_r,cv_l,cv_r)
    mix(eng, cv_l, cv_r, 7, 3, ancilla,8)
    cv_l, cv_r = word_perm(eng,cv_l,cv_r)

    for i in range(1,14):
        msg_e_l, msg_e_r= msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla2)
        msg_add(eng,msg_e_l,msg_e_r,cv_l,cv_r)
        mix(eng,cv_l,cv_r,23,59,ancilla,16 * i)
        cv_l, cv_r = word_perm(eng, cv_l, cv_r)

        msg_o_l, msg_o_r = msg_exp_odd(eng, msg_e_l, msg_e_r, msg_o_l, msg_o_r, ancilla2)
        msg_add(eng, msg_o_l, msg_o_r, cv_l, cv_r)
        mix(eng, cv_l, cv_r, 7, 3, ancilla, 16 * i + 8)
        cv_l, cv_r = word_perm(eng, cv_l, cv_r)

    msg_e_l, msg_e_r= msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla)
    msg_add(eng, msg_e_l, msg_e_r, cv_l, cv_r)

    return cv_l, cv_r

def final(eng,cv_l,cv_r):
    for i in range(8):
        CNOT64(eng, cv_r[64 * i:64 * (i + 1)], cv_l[64 * i:64 * (i + 1)])

def msg_exp_even(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla):
    msg_e_l = msg_perm(eng,msg_e_l)
    msg_e_r = msg_perm(eng, msg_e_r)

    for i in range(8):
        CDKM(eng, msg_o_l[64 * i :64 * (i + 1)], msg_e_l[64*i:64*(i+1)],ancilla[i],64)
        CDKM(eng, msg_o_r[64 * i: 64 * (i + 1)], msg_e_r[64 * i:64 * (i + 1)], ancilla[i+8], 64)

    return msg_e_l, msg_e_r

def msg_exp_odd(eng,msg_e_l,msg_e_r,msg_o_l,msg_o_r,ancilla):
    msg_o_l = msg_perm(eng,msg_o_l)
    msg_o_r = msg_perm(eng, msg_o_r)

    for i in range(8):
        CDKM(eng, msg_e_l[64 * i:64 * (i + 1)], msg_o_l[64 * i:64 * (i + 1)], ancilla[i], 64)
        CDKM(eng, msg_e_r[64 * i: 64 * (i + 1)], msg_o_r[64 * i:64 * (i + 1)], ancilla[i + 8], 64)

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
    for i in range(64):
        new_msg.append(msg[64*count +i])


def msg_add(eng,msg_l,msg_r,cv_l,cv_r):

    for i in range(8):
        CNOT64(eng, msg_l[64*i:64*(i+1)], cv_l[64*i:64*(i+1)])
        CNOT64(eng, msg_r[64 * i:64 * (i + 1)], cv_r[64 * i:64 * (i + 1)])


def mix(eng,cv_l,cv_r,alpha,beta,ancilla,sc_count):
    for i in range(8):
        CDKM(eng,cv_r[64 * i : 64 * (i + 1)], cv_l[64 * i : 64 * (i + 1)], ancilla[i],64)

    #rotation a
    for i in range(8):
        cv_l[64 * i : 64 * (i + 1)] = rotation(eng,cv_l[64 * i: 64 * (i + 1)],alpha)

    # xor with SC
    for i in range(8):
        Round_constant_XOR(eng,cv_l[64 * i : 64 * (i + 1)],SC[i+sc_count],64) # modify


    for i in range(8):
        CDKM(eng,cv_l[64 * i : 64 * (i + 1)], cv_r[64 * i : 64 * (i + 1)], ancilla[i],64)

    # rotation B
    for i in range(8):
        cv_r[64 * i: 64 * (i + 1)] = rotation(eng, cv_r[64 * i: 64 * (i + 1)], beta)
    #

    for i in range(8):
        CDKM(eng,cv_r[64 * i : 64 * (i + 1)], cv_l[64 * i : 64 * (i + 1)], ancilla[i],64)

    #
    # rotation gamma
    for i in range(1,8):
        cv_r[64 * i : 64 * (i + 1)] = rotation(eng,cv_r[64 * i : 64 * (i + 1)],gamma[i])

    # if (resource_check != 1):
    #     print_state(eng, cv_l, 128)
    #     print_state(eng, cv_l[0:64], 16)
    #     print_state(eng, cv_l[64:128], 16)
    #     print_state(eng, cv_l[128:192], 16)
    #     print_state(eng, cv_l[192:256], 16)
    #     print_state(eng, cv_l[256:320], 16)
    #     print_state(eng, cv_l[320:384], 16)
    #     print_state(eng, cv_l[384:448], 16)
    #     print_state(eng, cv_l[448:512], 16)
    #
    #     print("------------------------------------")
    #
    # if (resource_check != 1):
    #     print("gamma")
    #     print_state(eng, cv_r, 128)
    #     print_state(eng, cv_r[0:64], 16)
    #     print_state(eng, cv_r[64:128], 16)
    #     print_state(eng, cv_r[128:192], 16)
    #     print_state(eng, cv_r[192:256], 16)
    #     print_state(eng, cv_r[256:320], 16)
    #     print_state(eng, cv_r[320:384], 16)
    #     print_state(eng, cv_r[384:448], 16)
    #     print_state(eng, cv_r[448:512], 16)
    #
    #     print("------------------------------------")

def rotation(eng,cv,constant):
    new_cv =[]
    for i in range(64-constant,64):
        new_cv.append(cv[i])
    for i in range(64-constant):
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


def CNOT64(eng,a,b):
    for i in range(64):
        CNOT | (a[i], b[i])



def CDKM(eng, a, b, c, n):
    for i in range(n - 2):
        CNOT | (a[i + 1], b[i + 1])

    CNOT | (a[1], c)
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(n - 5):
        Toffoli_gate(eng, a[i + 1], b[i + 2], a[i + 2])
        CNOT | (a[i + 4], a[i + 3])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
    CNOT | (a[n - 2], b[n - 1])
    CNOT | (a[n - 1], b[n - 1])
    Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])

    for i in range(n - 3):
        X | b[i + 1]

    CNOT | (c, b[1])

    for i in range(n - 3):
        CNOT | (a[i + 1], b[i + 2])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])

    for i in range(n - 5):
        Toffoli_gate(eng, a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
        CNOT | (a[n - 2 - i], a[n - 3 - i])
        X | (b[n - 3 - i])

    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | b[2]
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | b[1]
    CNOT | (a[1], c)

    for i in range(n-1):
        CNOT | (a[i], b[i])

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

def Toffoli_gate(eng, a, b, c):
    Toffoli | (a, b, c)

    # if (resource_check):
    #     if (AND_check):
    #         ancilla = eng.allocate_qubit()
    #         H | c
    #         CNOT | (b, ancilla)
    #         CNOT | (c, a)
    #         CNOT | (c, b)
    #         CNOT | (a, ancilla)
    #         Tdag | a
    #         Tdag | b
    #         T | c
    #         T | ancilla
    #         CNOT | (a, ancilla)
    #         CNOT | (c, b)
    #         CNOT | (c, a)
    #         CNOT | (b, ancilla)
    #         H | c
    #         S | c
    #
    #     else:
    #         Tdag | a
    #         Tdag | b
    #         H | c
    #         CNOT | (c, a)
    #         T | a
    #         CNOT | (b, c)
    #         CNOT | (b, a)
    #         T | c
    #         Tdag | a
    #         CNOT | (b, c)
    #         CNOT | (c, a)
    #         T | a
    #         Tdag | c
    #         CNOT | (b, a)
    #         H | c
    # else:
    #     Toffoli | (a, b, c)

def Round_constant_XOR(eng, k, rc, bit):
    for i in range(bit):
        if (rc >> i & 1):
            X | k[i]
    # print_state(eng,k,bit)


global resource_check
global AND_check
global count
# count =0
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
print(count)
print('\n')
eng.flush()