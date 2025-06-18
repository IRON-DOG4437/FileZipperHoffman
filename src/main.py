# main.py
import os
import sys
from encoder.huffman_encoder import huffman_encode
from decoder.huffman_decoder import huffman_decode_main

def main():
    if len(sys.argv) != 4:
        input_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'input_file.txt')
        output_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'output_file.txt')
        decoded_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'decoded_file.txt')
        huffman_codes_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'huffman_codes.txt')
    
        huffman_encode(input_file, output_file,huffman_codes_file)
        huffman_decode_main(output_file, decoded_file, huffman_codes_file)
        sys.exit(1)
    else:
        command = sys.argv[1]
        input_file = os.path.join(os.path.dirname(__file__), '..', 'Data', sys.argv[2])
        output_file = os.path.join(os.path.dirname(__file__), '..', 'Data', sys.argv[3])
        huffman_codes_file = os.path.join(os.path.dirname(__file__), '..', 'Data', 'huffman_codes.txt')

        if command == 'compress':
            huffman_encode(input_file, output_file, huffman_codes_file)
        elif command == 'decompress':
            huffman_decode_main(input_file, output_file, huffman_codes_file)
        else:
            print("Invalid command. Use 'compress' or 'decompress'.")
            sys.exit(1)

if __name__ == '__main__':
    main()