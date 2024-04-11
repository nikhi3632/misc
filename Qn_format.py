'''
Fixed point representation:
	In general the input trained model is provided in floating point representation. 
    As the underlying hardware is either 8/16 bit precision, 
    there should be a way to convert each floating point value in the original model 
    to its equivalent fixed point representation. In this case the fixed point numbers 
    are represented in Qn format, which specifies the number of bits for integer and 
    fraction along with the sign bit. However, conversion from float to fixed point 
    representation will incur some loss as 8 bits may not be sufficient to exactly 
    represent the original float number. Highest importance is given to store the 
    integer part and the left over bits will be used for storing fraction. 
    In case of unsigned numbers, the sign bit is allocated for fraction. 
    If enough bits are not available to store fraction then it would be indicated using 
    a negative number. Few examples are given below.

Qn format representation: {sign, integer, fraction}

-3.4 in signed representation is {1,2,5}
3.4 in unsigned representation is {0,2,6}
250.45 in signed representation is {1,8,-1}

In the last example, the number is large enough that even the integer part can't fit 
in the allocated 8 bits. But it's represented as shown above to make sure 
no information is lost.

'''

def float_to_fixed_point(number, n, is_signed = True):
    if number < 0 and is_signed == False:
        raise "Negative numbers are always signed"
    # Calculate the sign bit
    num_sign_bits = 1 if (number < 0 or (number >= 0 and is_signed)) else 0
    
    # Calculate the absolute value of the number
    abs_number = abs(number)
    
    # Calculate the integer part and fractional part
    integer_part = int(abs_number)
    
    # Calculate the number of bits for the integer part
    num_integer_bits = 0
    while integer_part > 0:
        num_integer_bits += 1
        integer_part //= 2
    
    # Calculate the number of bits for the fractional part
    num_fraction_bits = n - num_sign_bits - num_integer_bits
    
    # Return the fixed-point representation as {sign, num_integer_bits, num_fraction_bits}
    return "{" + str(num_sign_bits) + ", " + str(num_integer_bits) + ", " + str(num_fraction_bits) + "}"


if __name__ == "__main__":
    n = 8

    number = -3.4
    fixed_point_representation = float_to_fixed_point(number, n)
    print(f"Fixed-point representation of {number} in Q{n} format:", fixed_point_representation)

    number = 3.4
    fixed_point_representation = float_to_fixed_point(number, n, is_signed=True)
    print(f"Fixed-point representation of {number} (signed) in Q{n} format:", fixed_point_representation)

    number = 3.4
    fixed_point_representation = float_to_fixed_point(number, n, is_signed=False)
    print(f"Fixed-point representation of {number} (unsigned) in Q{n} format:", fixed_point_representation)

    number = 250.45
    fixed_point_representation = float_to_fixed_point(number, n, is_signed=True)
    print(f"Fixed-point representation of {number} (signed) in Q{n} format:", fixed_point_representation)

    number = 250.45
    fixed_point_representation = float_to_fixed_point(number, n, is_signed=False)
    print(f"Fixed-point representation of {number} (unsigned) in Q{n} format:", fixed_point_representation)
