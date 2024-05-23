import sklearn

def train():
    with open('best_model.pt', 'w') as f:
        f.write('best model!! working!')
    with open('github.pt','w') as f:
        f.write('github actions works!!!!!')

if __name__ == '__main__':
    train()