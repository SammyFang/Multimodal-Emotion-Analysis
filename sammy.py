import subprocess

def run_script(script_path):
    try:
        result = subprocess.run(['python', script_path], text=True, capture_output=True, check=True)
        print(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")

def main():
    script1_path = './IER.py'
    script2_path = './SER.py'

    print("Running IER.py...")
    run_script(script1_path)

    print("Running SER.py...")
    run_script(script2_path)

if __name__ == '__main__':
    main()
