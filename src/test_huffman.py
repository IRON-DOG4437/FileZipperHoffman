import os
import shutil
import time
from encoder.huffman_encoder import huffman_encode
from decoder.huffman_decoder import huffman_decode_main, get_huffman_codes_from_file

# Set up the test environment by creating the necessary files and directories
def setup_test_environment(test_case, test_num):
    test_dir = os.path.abspath(os.path.join('test_data', f'test_case_{test_num}'))
    os.makedirs(test_dir, exist_ok=True)
    input_file = os.path.abspath(os.path.join(test_dir, 'input_file.txt'))
    output_file = os.path.abspath(os.path.join(test_dir, 'output_file.txt'))
    decoded_file = os.path.abspath(os.path.join(test_dir, 'decoded_file.txt'))
    huffman_codes_file = os.path.abspath(os.path.join(test_dir, 'huffman_codes.txt'))
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_case['input'])
    return input_file, output_file, decoded_file, huffman_codes_file

# Run a single test case
def run_test(test_num, test_case):
    input_file, output_file, decoded_file, huffman_codes_file = setup_test_environment(test_case, test_num)
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = f.read()
        execution_time, compression_ratio = huffman_encode(input_file, output_file, huffman_codes_file)
        huffman_codes = get_huffman_codes_from_file(huffman_codes_file)
        start_time = time.time()
        huffman_decode_main(output_file, decoded_file, huffman_codes_file)
        decode_time = time.time() - start_time
        with open(decoded_file, 'r', encoding='utf-8') as f:
            decoded_data = f.read()
        success = input_data == decoded_data
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        compression_percentage = ((input_size - output_size) / input_size) * 100 if input_size != 0 else 0
        test_result = {
            'test_num': test_num,
            'description': test_case['description'],
            'success': success,
            'input_size_kb': input_size / 1024,
            'output_size_kb': output_size / 1024,
            'compression_ratio': compression_ratio,
            'compression_percentage': compression_percentage,
            'encode_time': execution_time,
            'decode_time': decode_time,
            'message': 'Passed' if success else 'Failed: Decoded data does not match original.'
        }
    except FileNotFoundError as e:
        test_result = {
            'test_num': test_num,
            'description': test_case['description'],
            'success': False,
            'message': f'File not found: {e}'
        }
    except Exception as e:
        test_result = {
            'test_num': test_num,
            'description': test_case['description'],
            'success': False,
            'message': f'Error occurred: {e}'
        }
    return test_result

# Main function to run all test cases
def main():
    test_cases = [
        {'input': "hello", 'description': "Simple Text Case"},
        {'input': "abcdef", 'description': "All Unique Characters"},
        {'input': "aaaaaaaabbbbcccdde", 'description': "Highly Repetitive Text"},
        {'input': "Hello, World!", 'description': "Mixed Case and Special Characters"},
        {'input': ("This is a test.\nThis is only a test.\n" * 10).strip(), 'description': "Long String with Newlines"},
        {'input': "a" * 20, 'description': "Single Character Repeated"},
        {'input': "a a a a a a ", 'description': "Short String with Spaces"},
        {'input': "123abcABC", 'description': "Alphanumeric String"},
        {'input': "@#$%^&*()_+{}|:<>?", 'description': "Random Symbols and Punctuation"},
        {'input': "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.", 'description': "Realistic Paragraph with Repetition"},
    ]
    if os.path.exists('test_data'):
        shutil.rmtree('test_data')
    os.makedirs('test_data', exist_ok=True)
    passed = 0
    failed = 0
    total_encode_time = 0
    total_decode_time = 0
    total_compression_ratio = 0
    total_compression_percentage = 0
    results = []
    for i, test_case in enumerate(test_cases, 1):
        result = run_test(i, test_case)
        results.append(result)
        if result['success']:
            passed += 1
        else :
            failed += 1
        total_encode_time += result.get('encode_time', 0)
        total_decode_time += result.get('decode_time', 0)
        total_compression_ratio += result.get('compression_ratio', 0)
        total_compression_percentage += result.get('compression_percentage', 0)
    average_encode_time = total_encode_time / len(test_cases) if len(test_cases) > 0 else 0
    average_decode_time = total_decode_time / len(test_cases) if len(test_cases) > 0 else 0
    average_compression_ratio = total_compression_ratio / len(test_cases) if len(test_cases) > 0 else 0
    average_compression_percentage = total_compression_percentage / len(test_cases) if len(test_cases) > 0 else 0
    for res in results:
        print(f"Test {res['test_num']}: {res['description']}")
        print(f"  Status: {res['message']}")
        input_size_kb = res.get('input_size_kb', 'N/A')
        output_size_kb = res.get('output_size_kb', 'N/A')
        compression_ratio = res.get('compression_ratio', 'N/A')
        compression_percentage = res.get('compression_percentage', 'N/A')
        encode_time = res.get('encode_time', 'N/A')
        decode_time = res.get('decode_time', 'N/A')
        print(f"  Input Size: {input_size_kb:.2f} KB" if isinstance(input_size_kb, (int, float)) else f"  Input Size: {input_size_kb}")
        print(f"  Output Size: {output_size_kb:.2f} KB" if isinstance(output_size_kb, (int, float)) else f"  Output Size: {output_size_kb}")
        print(f"  Compression Ratio: {compression_ratio:.2f}" if isinstance(compression_ratio, (int, float)) else f"  Compression Ratio: {compression_ratio}")
        print(f"  Compression Percentage: {compression_percentage:.2f}%" if isinstance(compression_percentage, (int, float)) else f"  Compression Percentage: {compression_percentage}")
        print(f"  Encode Time: {encode_time:.4f} seconds" if isinstance(encode_time, (int, float)) else f"  Encode Time: {encode_time}")
        print(f"  Decode Time: {decode_time:.4f} seconds" if isinstance(decode_time, (int, float)) else f"  Decode Time: {decode_time}\n")
    print("Test Summary:")
    print(f"  Total Tests: {len(test_cases)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Average Encode Time: {average_encode_time:.4f} seconds")
    print(f"  Average Decode Time: {average_decode_time:.4f} seconds")
    print(f"  Average Compression Ratio: {average_compression_ratio:.2f}")
    print(f"  Average Compression Percentage: {average_compression_percentage:.2f}%")
    accuracy = (passed / len(test_cases)) * 100 if len(test_cases) > 0 else 0
    print(f"  Accuracy: {accuracy:.2f}%")

if __name__ == '__main__':
    main()