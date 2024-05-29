import subprocess

if __name__ == "__main__":
    with open('test_log.txt', 'w') as f:
        subprocess.run(["pytest", "--junitxml=test_results.xml"], stdout=f, text=True)