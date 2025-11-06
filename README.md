# End-to-End MLOps: Loan Default Prediction

This project demonstrates a complete, end-to-end MLOps workflow for building, deploying, and automating a machine learning model. The objective is to predict the probability of a customer defaulting on a personal loan, using a Flask web application deployed on AWS.

The entire process is automated via a CI/CD pipeline, ensuring that any new code pushed to the main branch is automatically tested, built, and deployed to a live environment.

![Flask App Screenshot](docs/images/flask_app_ui.png)

## MLOps Features Implemented

This project showcases several core MLOps practices:

- Version Control: The entire project is version-controlled using Git, with a clear commit history tracking every change.

- Experiment Tracking: All model training runs are meticulously logged and managed using MLflow, allowing for easy comparison and selection of the best model.

- Containerization: The Flask application is packaged into a portable and reproducible Docker image, encapsulating the code, model, and all dependencies.

- Continuous Integration & Continuous Deployment (CI/CD): An automated GitHub Actions pipeline handles the entire workflow:

- CI: Installs dependencies, runs data processing and training scripts to generate model artifacts.

- CD: Builds a Docker image, pushes it to Amazon ECR, and deploys it as a live service on Amazon ECS (Fargate).

- Cloud Deployment: The final application is deployed on AWS, making it accessible via a public URL.

## Project Structure

```plaintext
.
├── .github/workflows/      # Contains the GitHub Actions CI/CD pipeline (main.yml)
├── data/
│   ├── processed/          # Processed data (X_train, y_train, etc.) - Ignored by Git
│   └── loan_deafult.csv    # The raw dataset
├── docs/
│   └── images/             # Screenshots for the final presentation
├── models/                 # The final trained model artifact (model.pkl) - Ignored by Git
├── notebooks/              # Jupyter notebooks for EDA and experimentation
├── processors/             # The saved data scaler (scaler.joblib) - Ignored by Git
├── src/
│   ├── data_processing.py  # Script to clean data and create features
│   └── train.py            # Script to train models and log with MLflow
├── templates/
│   └── index.html          # HTML template for the Flask app UI
├── app.py                  # The Flask web application
├── Dockerfile              # Instructions to build the application's Docker image
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## How to Run This Project

### Prerequisites

- Python 3.11.0
- Conda environment to manage libraries
- Cursor or VSCode for code edting
- Github
- Xterm
- MLFlow
- Docker Desktop
- An AWS account with the AWS CLI configured

### 1. Local Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/adamfaik/loan-default-prediction
    cd loan-default-prediction
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    Update Python version in venv/pyvenv.cfg file to 3.11.5 in /opt path

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### 2. Running the Key Scripts

1.  **Process the data:**

    This script will generate the cleaned and scaled data in the `data/processed/` folder and the `scaler.joblib` file.
    ```bash
    python src/data_processing.py
    ```

2.  **Train the models:**

    First, activate venv and then run MLFlow server with host and port (5001), with database pointer to store information. On Apple OS, port 5000 is used by ControlCenter (macOS Airplay), so we use a different port 5001.

    ```bash
    source venv/bin/activate && mlflow server --host 127.0.0.1 --port 5001 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
    ```

    Next, export the path for MLFlow as follows:

    ```bash
    export MLFLOW_TRACKING_URI="http://127.0.0.1:5001"
    ```

    Then, run the training script. This will create the `mlruns/` directory and log all experiments.

    ```bash
    python src/train.py
    ```

    You can view the results at `http://127.0.0.1:5001`.

### 3. Running the Application

There are two ways to run the web application:

**A. Locally with Flask:**

This requires you to manually copy the best `model.pkl` from the `mlruns` directory into the `models/` folder.

```bash
# Launch the local Flask server
python app.py
```

The app will be available at `http://127.0.0.1:4999`.

**B. Using Docker (Recommended):**

This method simulates the production environment.

```bash
# 1. Run Docker daemon
open -a Docker

# 2. Build the Docker image
docker build -t loan-app .

# 2. Run the container
docker run -d -p 3000:4999 --name loan-app loan-default-prediction
```

The app will be available at `http://localhost:3000`. Port 4999 refers to the interal port that the Flask app is listening on. You can diagnose this by running the command `docker logs loan-ap` to find out which port is being used.




## AWS Role & Permissions

### IAM Policy

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ECRPermissions",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:DescribeRepositories",
                "ecr:DescribeImages",
                "ecr:BatchDeleteImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ECSPermissions",
            "Effect": "Allow",
            "Action": [
                "ecs:DescribeTaskDefinition",
                "ecs:RegisterTaskDefinition",
                "ecs:UpdateService",
                "ecs:DescribeServices",
                "ecs:DescribeClusters",
                "ecs:ListTasks",
                "ecs:DescribeTasks",
                "ecs:RunTask",
                "ecs:StopTask"
            ],
            "Resource": "*"
        },
        {
            "Sid": "IAMPassRole",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::*:role/ecsTaskExecutionRole",
                "arn:aws:iam::*:role/ecsTaskRole"
            ]
        }
    ]
}
```

🏗️ AWS Managed Policies (Alternative)
You can also use these AWS managed policies:
For ECR:
AmazonEC2ContainerRegistryPowerUser - Full access to ECR
AmazonEC2ContainerRegistryReadOnly - Read-only access (not sufficient for push)
For ECS:
AmazonECS_FullAccess - Full access to ECS
AmazonECS_TaskExecutionRolePolicy - For task execution
🔧 Setup Instructions
1. Create IAM User/Role:
```bash
# Create IAM user
aws iam create-user --user-name github-actions-user

# Attach policy
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::YOUR-ACCOUNT:policy/GitHubActionsPolicy
```

## CI/CD Pipeline

The CI/CD pipeline is defined in `.github/workflows/main.yml`. It is triggered on every `push` to the `main` branch and performs the following jobs:

1. `ci` **(Build, Test, and Create Artifacts)**:

    - Installs dependencies.

    - Runs the data processing and training scripts to generate the `scaler.joblib` and `model.pkl` files.

    - Uploads all necessary application files as a shareable artifact.

2. `cd` **(Deploy to AWS ECS)**:

    - Downloads the artifacts from the `ci` job.

    - Builds a Docker image.

    - Pushes the image to a private repository in Amazon ECR.

    - Deploys a new revision of the application to a running service on Amazon ECS (Fargate).

To use this pipeline, the following secrets must be configured in the GitHub repository's `Settings > Secrets and variables > Actions`:

- `AWS_ACCESS_KEY_ID`

- `AWS_SECRET_ACCESS_KEY`

- `ECS_CLUSTER`

- `ECS_SERVICE`

- `ECS_TASK_DEFINITION`