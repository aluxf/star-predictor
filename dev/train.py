import subprocess
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from dataset import create_dataset
import joblib
from ray import tune
import ray

def train(df):
    y = df['stars']
    X = df.drop(columns=['stars'])

    s = StandardScaler()
    X = s.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = [
        XGBRegressor(),
        LinearRegression(),
        RandomForestRegressor(random_state=42),
        GradientBoostingRegressor(random_state=42),
    ]
    
    # Initialize Ray
    ray.init()

    # Define a Ray Tune training function
    def train_model(config, data):
        model = config['model']
        X_train, y_train = data['X_train'], data['y_train']
        cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='r2').mean()
        return { "score" : cv_score}

    search_space = {
        "model": tune.grid_search(models),
    }

    dataset = {
        "X_train": X_train,
        "y_train": y_train,
    }
    tuner = tune.Tuner(tune.with_parameters(train_model, data=dataset), param_space=search_space)
    result = tuner.fit()
    best_model = result.get_best_result(metric="score", mode="max").config["model"]

    best_model.fit(X_train, y_train)
    test_score = best_model.score(X_test, y_test)
    print(f"Test R^2 Score: {test_score}")
    # Shutdown Ray
    ray.shutdown()

    joblib.dump(best_model, 'best_model.pkl')


if __name__ == '__main__':
    df = create_dataset()
    train(df)
    # Run the Bash script
    try:
        subprocess.run(['bash', "push-to-prod"], check=True)
        print("Successfully pushed to prod")
    except subprocess.CalledProcessError as e:
        print("Error executing script:", e)