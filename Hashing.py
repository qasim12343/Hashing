
sboxes = read_sboxes('sbox.txt')


def HashAlgo(plain, subKeys, salt, no_workFactor):
    pass


def workFactor(plain, key, salt):
    pass


def Box(key, plain):
    pass


def round(left, right, key):
    op1 = int(left, 2) ^ int(key, 2)
    op2 = int(w(op1), 2) ^ int(right, 2)


def w(input_32bit):
    subs = [input_32bit[i:i+8] for i in range(0, 32, 8)]
    s0 = subs[0]
    s2 = subs[1]
    s3 = subs[2]
    s4 = subs[3]

    oss = [sbox(s0), sbox(s1), sbox(s2), sbox(s3)]
    op1 = (int(sbox(s0), 2)+int(sbox(s1), 2)) % (2**32)
    op2 = op1 ^ int(sbox(s2), 2)
    op3 = (op2 + int(sbox(s3), 2)) % (2**32)

    return bin(op3)[2:].zfill(32)


def sbox(b):
    row = b[6]+b[5]+b[4]+b[3]+b[2]  # b1,b2,b3,b4,b5
    col = b[7]+b[0]+b[1]  # b0,b6, b7
    n_row = int(row, 2)
    n_col = int(col, 2)
    return hex_to_binary(sboxes[n_row][n_col])


def read_sboxes(file_path):
    with open(file_path, 'r') as file:
        sboxes = [[] for _ in range(4)]
        sbox_index = 0
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace
            if line.startswith("S-box"):
                sbox_index = int(line.split()[1]) - 1
            else:
                hex_values = line.split()
                sboxes[sbox_index].extend(hex_values)
    return sboxes


def hex_to_binary(hex_value):
    return bin(int(hex_value, 16))[2:].zfill(32)
