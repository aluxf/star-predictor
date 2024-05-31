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
import json

rf_search = {
    'n_estimators': tune.randint(100, 300),
    'max_depth': tune.randint(10, 30),
    'min_samples_split': tune.randint(2, 5),
    'min_samples_leaf': tune.randint(1, 5),
    'random_state': 42
}


num_samples = 100

def train(df):
    y = df['stars']
    X = df.drop(columns=['stars'])

    s = StandardScaler()
    X = s.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with open("model_results.json", "r") as f:
        results = json.loads(f.read())
        
    # Initialize Ray
    ray.init()
    
    best_model = joblib.load("best_model.pkl")

    # Define a Ray Tune training function
    def train_model(config, data):
        model = config["model"]
        model.set_params(**config["hyperparams"])
        X_train, y_train = data['X_train'], data['y_train']
        cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='r2').mean()
        return { "score" : cv_score}

    search_space = {
        "model" : best_model
    }
    if results['model'] == "RandomForestRegressor":
        search_space["hyperparams"] = rf_search
        print("rf_search")
    
    dataset = {
        "X_train": X_train,
        "y_train": y_train,
    }
    tuner = tune.Tuner(
        tune.with_parameters(train_model, data=dataset), 
        param_space=search_space,
        tune_config=tune.TuneConfig(
                num_samples=num_samples,
                metric="score",
                mode="max"
            ))
    result = tuner.fit()
    best_config = result.get_best_result(metric="score", mode="max").config["hyperparams"]

    best_model.set_params(**best_config)
    best_model.fit(X_train, y_train)
    test_score = best_model.score(X_test, y_test)
    print(f"Best model: {best_model.__class__,__name__}")
    print(f"Test R^2 Score: {test_score}")
    print(best_config)

    # Shutdown Ray
    ray.shutdown()

    joblib.dump(best_model, '/app/best_model.pkl')
    results = {
        "model": best_model.__class__.__name__,
        "test_score": test_score
    }
    with open("/app/model_results.json", "w") as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    df = create_dataset()
    train(df)