import sklearn
import subprocess

def train():
    with open('best_model.pt', 'w') as f:
        f.write('best model!! working :DDD')
    with open('github.pt','w') as f:
        f.write('github actions works!!!!!')

if __name__ == '__main__':
    train()
    # Run the Bash script
    try:
        subprocess.run(['bash', "push-to-prod"], check=True)
        print("Successfully pushed to prod")
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e)