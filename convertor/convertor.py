import sys
import os
import json
import yaml


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
    input_file, output_file = parse_args()
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

def read_json(file_path):
    try:
        with open(file_path,'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON:{e}")
        sys.exit(1)

def write_json(data,file_path):
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing JSON {e}")
        sys.exit(1)

def read_yaml(file_path):
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML{e}")
        sys.exit(1)
