import sys
import os

def parse_args():
    if len(sys.argv) !=3:
        print("Error: Incorrect number of arguments")
        print("Usage: program.exe input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        sys.exit(1)

    return input_file, output_file


if __name__ == "__main__":
    input_file,output_file =parse_args()
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
