import copy
Subbytes = [
    ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
    ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
    ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
    ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
    ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
    ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
    ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
    ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
    ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
    ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
    ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
    ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
    ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
    ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
    ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
    ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
]   
MixColumn = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]

#This function takes a character x as input, converts it to its ASCII code, and then returns its hexadecimal representation with a leading 0 if necessary.
def hexdec(x):
    x1 = ord(x)
    z = str(hex(x1)).split('x')
    if(len(z[1]) != 2):
        z[1] = '0'+z[1]
    return z[1].upper()
#Takes two 4-byte strings x and y, treats them as hexadecimal numbers, performs a bitwise XOR operation on them, and returns the result as a 4-byte string.
def XOR(x, y):
    z = []
    for i in range(4):
        temp = str(hex(int(x[i],16)^int(y[i],16)).split('x')[-1]).upper()
        if(len(temp) != 2):
            temp = '0'+temp
        z.append(temp)
    return z
#Takes a 16-byte key and generates a list of 44 4-byte words used in the AES encryption process.
def EntendKey(KEY):
    l1 = list(KEY)
    l2 = [hexdec(i) for i in l1]
    roundKey = []
    roundKey.append(l2)
    RC = ['01', '02', '04', '08', '10', '20', '40', '80', '1B', '36']
    rc = [int(i,16) for i in RC]
    for i in range(10):
        w3 = [roundKey[-1][13], roundKey[-1][14], roundKey[-1][15], roundKey[-1][12]]
        subtituteByte = []
        for j in range(4):
            s1 = int(w3[j][0],16)
            s2 = int(w3[j][1],16)
            subtituteByte.append(Subbytes[s1][s2])
        subtituteByte[0] = str(hex(int(subtituteByte[0],16)^int(rc[i]))).split('x')[-1].upper()
        if len(subtituteByte[0]) != 2:
            subtituteByte[0] = '0'+subtituteByte[0]
        w4 = XOR(roundKey[-1][0:4],subtituteByte)
        w5 = XOR(roundKey[-1][4:8], w4)
        w6 = XOR(roundKey[-1][8:12], w5)
        w7 = XOR(roundKey[-1][12:16], w6)
        w_final = w4 + w5 + w6 + w7
        roundKey.append(w_final)
    return roundKey
#Takes two 4x4 matrices x and y, treats each element as a 1-byte hexadecimal number, 
# performs a bitwise XOR operation on each element, and returns the result as a 4x4 matrix.
def XOR1(x, y):
    z = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    for i in range(4):
        for j in range(4):
            temp = str(hex(int(x[i][j],16)^int(y[i][j],16)).split('x')[-1]).upper()
            if(len(temp) != 2):
                temp = '0'+temp
            z[i][j] = temp
    return z
#Takes a single 1-byte hexadecimal number x and performs a left shift operation on it, returning the result as a 1-byte hexadecimal number.
def shift(x):
    m = str(hex(int(x, 16)<<1)).split('x')[-1].upper()
    r = ''
    if(len(m)==3):
        m = str(hex(int(m,16)^283)).split('x')[-1].upper()
    if(len(m) != 2):
        m = '0'+m
    r = m[-2]+m[-1]
    return r
#Takes two 1-byte hexadecimal numbers x and y, performs a bitwise XOR operation on them, and returns the result as a 1-byte hexadecimal number.
def hexdecXOR(x, y):
    z = str(hex(int(x, 16)^int(y, 16))).split('x')[-1].upper()
    if(len(z) != 2):
        z = '0'+z
    return z
#Takes a single 1-byte hexadecimal number x, performs a left shift operation on it, 
#and then performs a bitwise XOR operation with the original number x, returning the result as a 1-byte hexadecimal number.
def shift_AND_XOR(x):
    m = shift(x)
    n = hexdecXOR(m ,x)
    return n
#Takes two 4x4 matrices x and y, treats each element as a 1-byte hexadecimal number,
#performs a multiplication operation on each element using the AES-specific Galois field multiplication, and returns the result as a 4x4 matrix.
def multiplication(x,y):
    z = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    for i in range(4):
        for j in range(4):
            m = '00'
            #each element of matrix x and performs the corresponding GF multiplication of the elements of matrix y
            for k in range(4):
                if(x[i][k] == 2):
                    a = shift(y[k][j])
                    m = hexdecXOR(m,a)
                elif(x[i][k] == 1):
                    m = hexdecXOR(m, y[k][j])
                elif(x[i][k] == 3):
                    m = hexdecXOR(m, shift_AND_XOR(y[k][j]))
                elif(x[i][k] == 9):
                    a = shift(shift(shift(y[k][j])))
                    b = hexdecXOR(a,y[k][j])
                    m = hexdecXOR(m, b)
                elif(x[i][k] == 11):
                    a = shift(shift(shift(y[k][j])))
                    b = shift(y[k][j])
                    c = hexdecXOR(a, b)
                    d = hexdecXOR(c, y[k][j])
                    m = hexdecXOR(m, d)
                elif(x[i][k] ==13):
                    a = shift(shift(shift(y[k][j])))
                    b = shift(shift(y[k][j]))
                    c = hexdecXOR(a, b)
                    d = hexdecXOR(c, y[k][j])
                    m = hexdecXOR(m, d)
                elif(x[i][k] == 14):
                    a = shift(shift(shift(y[k][j])))
                    b = shift(shift(y[k][j]))
                    c = shift(y[k][j])
                    d = hexdecXOR(a, b)
                    e = hexdecXOR(c, d)
                    m = hexdecXOR(m, e)
            z[i][j] = m
    return z
def encrypt(message, roundKey):
    message_list = list(message)
    message_list1 = [hexdec(i) for i in message_list]
    state_matrix = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    temp_key = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    k = 0
    for i in range(4):
        for j in range(4):
            state_matrix[j][i] = message_list1[k]
            k = k+1
    k = 0
    for i in range(4):
        for j in range(4):
            temp_key[j][i] = roundKey[0][k]
            k = k+1
    #initially perform addition of round key
    state_matrix = XOR1(state_matrix, temp_key)
    for i in range(10):
        #perform substitution
        for j in range(4):
            for k in range(4):
                m = int(state_matrix[j][k][0], 16)
                n = int(state_matrix[j][k][1], 16)
                state_matrix[j][k] =  Subbytes[m][n]
        temp = copy.deepcopy(state_matrix)
        #shift operation
        for j in range(4):
            for k in range(4):
                state_matrix[j][k] = temp[j][(k+j)%4]
        # mix column for round 1 to 9 
        if(i != 9):
            state_matrix = multiplication(MixColumn, state_matrix)
        z = [
            [roundKey[i+1][0], roundKey[i+1][4], roundKey[i+1][8], roundKey[i+1][12]],
            [roundKey[i+1][1], roundKey[i+1][5], roundKey[i+1][9], roundKey[i+1][13]],
            [roundKey[i+1][2], roundKey[i+1][6], roundKey[i+1][10], roundKey[i+1][14]],
            [roundKey[i+1][3], roundKey[i+1][7], roundKey[i+1][11], roundKey[i+1][15]],
        ]
        #add round key
        state_matrix = XOR1(state_matrix, z)
    cipherText = ''
    for i in range(4):
        for j in range(4):
            cipherText += state_matrix[j][i]
    return cipherText

def message_Conversion(x):
    m = int(x,16)
    return chr(m)
KEY = 'Thats my Kung Fu'
message = 'Two One Nine Two'
roundKey = EntendKey(KEY)
print("Cipher Text")
cipherText = encrypt(message, roundKey)
print(cipherText)
