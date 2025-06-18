import argparse
import time

#Defines a Node class for a Huffman tree, with attributes for character, frequency, and left and right child nodes.
class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None


#Reads a file and returns a dictionary of Huffman codes, where each key is a character and each value is its corresponding Huffman code.
def get_huffman_codes_from_file(huffman_codes_file):
    huffman_codes = {}
    with open(huffman_codes_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line and ':' in line:
                char, code = line.split(':', 1)
                if char == '':
                    char = ' '
                huffman_codes[char] = code
    huffman_codes['__EOF__'] = '11111111'
    return huffman_codes

#Decodes encoded data using Huffman codes, replacing each code with its corresponding character.
def decode_data(encoded_data, huffman_codes):
    decoded_data = ''
    temp = ''
    reverse_huffman_codes = {code: char for char, code in huffman_codes.items()}
    for bit in encoded_data:
        temp += bit
        if temp in reverse_huffman_codes:
            char = reverse_huffman_codes[temp]
            if char == '__EOF__':
                break
            decoded_data += char
            temp = ''
    return decoded_data

#Replaces special character placeholders with their original characters in the decoded data.
def postprocess_output(text):
    special_chars = [
        ('@', '__SPECIAL_AT'),
        ('#', '__SPECIAL_HASH'),
        ('$','__SPECIAL_DOLLAR'),
        ('%', '__SPECIAL_PERCENT'),
        ('^', '__SPECIAL_CARET'),
        ('&', '__SPECIAL_AND'),
        ('*', '__SPECIAL_STAR'),
        ('(', '__SPECIAL_LEFT_PAREN'),
        (')', '__SPECIAL_RIGHT_PAREN'),
        ('_', '__SPECIAL_UNDERSCORE'),
        ('+', '__SPECIAL_PLUS'),
        ('{', '__SPECIAL_LEFT_BRACE'),
        ('}', '__SPECIAL_RIGHT_BRACE'),
        ('|', '__SPECIAL_VERTICAL_BAR'),
        (':', '__SPECIAL_COLON'),
        ('<', '__SPECIAL_LEFT_ANGLE_BRACKET'),
        ('>', '__SPECIAL_RIGHT_ANGLE_BRACKET'),
    ]
    for char, special_char in special_chars:
        text = text.replace(special_char, char)
    return text.replace('__NEWLINE__', '\n')

#Decodes an encoded file using Huffman codes, removing padding, decoding the data, and writing the decoded data to an output file.
def huffman_decode(input_file, output_file, huffman_codes):
    start_time = time.time()
    with open(input_file, 'rb') as input_file:
        encoded_bytes = input_file.read()
    padding = encoded_bytes[0]
    encoded_data = ''.join(format(byte, '08b') for byte in encoded_bytes[1:])
    if padding > 0:
        encoded_data = encoded_data[:-padding]
    decoded_data = decode_data(encoded_data, huffman_codes)
    decoded_data = postprocess_output(decoded_data)
    with open(output_file, 'w') as output_file:
        output_file.write(decoded_data)
    end_time = time.time()
    execution_time = end_time - start_time
    return decoded_data, execution_time

def huffman_decode_main(input_file, output_file, huffman_codes_file):
    huffman_codes = get_huffman_codes_from_file(huffman_codes_file)
    huffman_decode(input_file, output_file, huffman_codes)

def main():
    parser = argparse.ArgumentParser(description='Huffman Decoder')
    parser.add_argument('command', choices=['decompress'], help='Command to execute')
    parser.add_argument('input_file', help='Input file to read compressed data')
    parser.add_argument('codes_file', help='Output file to write decompressed data')
    args = parser.parse_args()

    if args.command == 'decompress':
        input_file = args.input_file
        huffman_codes_file = args.codes_file
        output_file = 'Decompressed_file.txt'  
        start_time = time.time()
        huffman_decode_main(input_file, output_file, huffman_codes_file)
        decode_time = time.time() - start_time
        print(f"Decompression time: {decode_time:.4f} seconds")

if __name__ == '__main__':
    main()
    