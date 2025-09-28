import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import mlflow
import mlflow.sklearn
import os

# MLflow setup
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Housing_Price_Experiment")

def main():
    # Load dataset
    df = pd.read_csv(os.path.join("data", "housing.csv"))
    X = df[["area"]]
    y = df["price"]

    # Split data
    test_size = 0.2
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Start MLflow run
    with mlflow.start_run():
        # Parameters
        lr = 0.01
        epochs = 100
        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("epochs", epochs)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Metrics
        score = model.score(X_test, y_test)
        print("Model R^2 Score:", score)
        mlflow.log_metric("r2_score", score)

        # Save local copy
        os.makedirs("model", exist_ok=True)
        joblib.dump(model, "model/model.pkl")

        # Log local copy
        mlflow.log_artifact("model/model.pkl")

        # Log model to MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="linear_regression_model",
            input_example=X_test[:1]
        )

if __name__ == "__main__":
    main()
