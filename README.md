# File Zipper using Greedy Hoffman Encoding

## 📌 Project Summary  
**FileZipper** is a lightweight file compression utility that applies the Greedy Huffman algorithm to reduce file sizes without any data loss. The project showcases the efficiency of greedy methods in real-world applications, particularly in balancing compression ratio and runtime performance.

---

## 🚀 Features  
- **File Compression:** Efficiently compresses large text files.
- **File Decompression:** Reconstructs original files from compressed versions.
- **Greedy Strategy Demonstration:** Highlights Huffman encoding's application.
- **Performance Trade-off Insights:** Understand the relationship between compression depth and processing time.

---

## ⚙️ How It Works  
Huffman coding is a lossless compression technique that assigns shorter binary representations to frequently occurring characters and longer ones to less frequent characters.

**Compression Workflow:**
1. **Frequency Count:** Count occurrences of each character in the file.
2. **Build Huffman Tree:** Generate a binary tree based on frequency.
3. **Assign Codes:** Allocate binary codes – shorter for frequent, longer for rare.
4. **Encode File:** Convert file content into binary based on these codes.
5. **Decode File:** Use the Huffman tree to reconstruct the original content.

---

## 🛠 Installation

Clone this repository:
```bash
git clone https://github.com/IRON-DOG4437/FileZipperHoffman.git
cd FileZipperHoffman
```

## Usage
📦 Compress a File
Option 1 – From encoder folder:
```bash
cd src/encoder
python huffman_encoder.py compress <input_file.txt>
```
Option 2 – From src folder:
```bash
cd src
python -B main.py compress <input_file.txt> <output_file.txt>
```
The -B flag disables Python bytecode file creation.

🔓 Decompress a File
Option 1 – From decoder folder:
```bash
cd src/decoder
python huffman_decoder.py decompress <compressed_file.txt> <huffman_codes_file.txt>
```
Option 2 – From src folder:
```bash
cd src
python -B main.py decompress <compressed_file.txt> <decoded_file.txt>
```

## Example Files
input_file.txt: Example input for testing.
output_file.txt: Output of compression.
decoded_file.txt: File output after decompression (should match original).`

## Testing
Run automated test cases from the src directory:
```bash
python -B test_huffman.py
```
This runs 12 unit tests and logs results to testResultlog.txt.
