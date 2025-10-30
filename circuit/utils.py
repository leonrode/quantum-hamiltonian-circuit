import numpy as np
def ket_label_q0_first(sv):
    n = int(np.log2(len(sv)))
    idx = int(np.argmax(np.abs(sv)**2))
    b = f"{idx:0{n}b}"
    return f"|{b[::-1]}>"