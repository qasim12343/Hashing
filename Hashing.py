
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
                sboxes[sbox_index].extend([hex_values])
    return sboxes


def hex_to_binary(hex_value):
    return bin(int(hex_value, 16))[2:].zfill(32)


sboxes = read_sboxes('sbox.txt')
keys = '''0x243F6A88 0x85A308D3 0x13198A2E 0x03707344 0xA4093822 0x299F31D0 0x082EFA98 0xEC4E6C89 0x452821E6 0x38D01377 0xBE5466CF 0x34E90C6C 0xC0AC29B7 0xC97C50DD 0x3F84D5B5 0xB5470917 0x9216D5D9 0x8979FB1B 0x38D01377 0xA4093822 0xEC4E6C89 0x243F6A88 0x13198A2E 0x85A308D3 0x082EFA98 0x85A308D3 0xBE5466CF 0x03707344 0x243F6A88 0x452821E6 0x85A308D3 0x38D01377'''
keys = keys.split(' ')
keys = [bin(int(a, 16))[2:].zfill(32) for a in keys]


def sbox(b, number):
    row = b[1] + b[2] + b[3] + b[4] + b[5]  # b1,b2,b3,b4,b5
    col = b[0]+b[6]+b[7]  # b0,b6, b7
    n_row = int(row, 2)
    n_col = int(col, 2)
    # print(sboxes[number][n_row][n_col])
    return bin(int(sboxes[number][n_row][n_col], 16))[2:].zfill(32)


s = sbox('10101111', 0)


def w(input_32bit):
    subs = [input_32bit[i:i+8] for i in range(0, 32, 8)]
    s0 = subs[0]
    s1 = subs[1]
    s2 = subs[2]
    s3 = subs[3]

    op1 = (int(sbox(s0, 0), 2)+int(sbox(s1, 1), 2)) % (2**32)
    op2 = op1 ^ int(sbox(s2, 2), 2)
    op3 = (op2 + int(sbox(s3, 3), 2)) % (2**32)

    return bin(op3)[2:].zfill(32)


def algorithm(plaintext,  salt, work_Factor):

    plain = bin(int(plaintext, 16))[2:].zfill(64)
    salt = bin(int(salt, 16))[2:].zfill(64)
    c = workFactor(plain, keys, salt)
    for _ in range(2**work_Factor - 1):
        c = workFactor(c, keys, salt)
    return hex(int(c, 2))


def workFactor(plain, keys, salt):
    op1 = box(plain, keys)
    op2 = int(op1, 2) ^ int(salt, 2)
    return bin(op2)[2:].zfill(64)


def box(plain, keys):
    left, right = round(plain[0:32], plain[32:], keys[0])
    for i in range(31):
        left, right = round(left, right, keys[i+1])
    return lastround(left, right, keys[30], keys[31])


def round(left, right, key):
    op1 = bin(int(left, 2) ^ int(key, 2))[2:].zfill(32)
    op2 = int(w(op1), 2) ^ int(right, 2)
    right = left
    left = bin(op2)[2:].zfill(32)

    return [left, right]


def lastround(left, right, key30, key31):
    op1 = int(left, 2) ^ int(key30, 2)
    op2 = int(right, 2) ^ int(key31, 2)
    left = bin(op2)[2:].zfill(32)
    right = bin(op1)[2:].zfill(32)
    return left + right


def main():
    plaintext = input()
    salt = input()
    work_factor = int(input())

    result = algorithm(plaintext, salt, work_factor)
    print(result)


main()
