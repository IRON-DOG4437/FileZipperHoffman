import collections
import heapq
import os
import time
import argparse

class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

# Calculate the frequency of each character in the input file
def calculate_frequencies(input_file):
    with open(input_file, 'r') as file:
        text = file.read()
    text = preprocess_input(text)
    frequency_dict = collections.defaultdict(int)
    for char in text:
        frequency_dict[char] += 1
    return frequency_dict

# Build a Huffman tree from the frequency dictionary
def build_huffman_tree(frequency_dict):
    priority_queue = []
    for char, frequency in frequency_dict.items():
        node = Node(char, frequency)
        heapq.heappush(priority_queue, node)
    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged_node = Node(None, node1.frequency + node2.frequency)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(priority_queue, merged_node)
    return priority_queue[0]

# Generate Huffman codes from the Huffman tree
def generate_huffman_codes(root, current_code, huffman_codes):
    if root is None:
        return
    if root.char is not None:
        huffman_codes[root.char] = current_code
    generate_huffman_codes(root.left, current_code + '0', huffman_codes)
    generate_huffman_codes(root.right, current_code + '1', huffman_codes)

# Get the Huffman codes from the Huffman tree
def get_huffman_codes(root):
    huffman_codes = {}
    generate_huffman_codes(root, '', huffman_codes)
    if len(huffman_codes) == 1:
        single_char = list(huffman_codes.keys())[0]
        huffman_codes[single_char] = '0'
    huffman_codes['__EOF__'] = '11111111'
    return huffman_codes

# Preprocess the input text by replacing special characters
def preprocess_input(text):
    special_chars = str.maketrans({
        '@': '__SPECIAL_AT',
        '#': '__SPECIAL_HASH',
        '$': '__SPECIAL_DOLLAR',
        '%': '__SPECIAL_PERCENT',
        '^': '__SPECIAL_CARET',
        '&': '__SPECIAL_AND',
        '*': '__SPECIAL_STAR',
        '(': '__SPECIAL_LEFT_PAREN',
        ')': '__SPECIAL_RIGHT_PAREN',
        '_': '__SPECIAL_UNDERSCORE',
        '+': '__SPECIAL_PLUS',
        '{': '__SPECIAL_LEFT_BRACE',
        '}': '__SPECIAL_RIGHT_BRACE',
        '|': '__SPECIAL_VERTICAL_BAR',
        ':': '__SPECIAL_COLON',
        '<': '__SPECIAL_LEFT_ANGLE_BRACKET',
        '>': '__SPECIAL_RIGHT_ANGLE_BRACKET',
    })
    text = text.translate(special_chars)
    return text.replace('\n', '__NEWLINE__')

# Encode the input data using Huffman codes
def encode_data(input_file, output_file, huffman_codes):
    with open(input_file, 'r') as input_file:
        text = input_file.read()
    text = preprocess_input(text)
    encoded_data = ''.join(huffman_codes[char] for char in text)
    padding = 8 - (len(encoded_data) % 8)
    padding_info = "{0:08b}".format(padding)
    encoded_data += '0' * padding
    with open(output_file, 'wb') as output_file:
        byte_array = bytearray()
        byte_array.append(int(padding_info, 2))
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            byte_array.append(int(byte, 2))
        output_file.write(byte_array)

# Write the Huffman codes to a file
def write_huffman_codes_to_file(huffman_codes, file_path):
    with open(file_path, 'w') as file:
        for char, code in huffman_codes.items():
            file.write(f'{char}:{code}\n')
        # file.write(f'__EOF__:{huffman_codes["__EOF__"]}')

# Perform Huffman encoding on the input file
def huffman_encode(input_file, output_file, huffman_codes_file):
    start_time = time.time()
    frequency_dict = calculate_frequencies(input_file)
    root = build_huffman_tree(frequency_dict)
    huffman_codes = get_huffman_codes(root)
    write_huffman_codes_to_file(huffman_codes, huffman_codes_file)
    encode_data(input_file, output_file, huffman_codes)
    end_time = time.time()
    execution_time = end_time - start_time
    input_size = os.path.getsize(input_file)
    output_size = os.path.getsize(output_file)
    compression_ratio = input_size / output_size if output_size != 0 else 0
    return execution_time, compression_ratio

def main():
    parser = argparse.ArgumentParser(description='Huffman Encoder')
    parser.add_argument('command', choices=['compress'], help='Command to execute')
    parser.add_argument('input_file', help='Input file to compress')
    args = parser.parse_args()

    if args.command == 'compress':
        input_file = args.input_file
        output_file = 'Compressed_file.txt'
        huffman_codes_file = 'huffman_codes.txt'
        execution_time, compression_ratio = huffman_encode(input_file, output_file, huffman_codes_file)
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Execution time: {execution_time:.4f} seconds")

if __name__ == '__main__':
    main()