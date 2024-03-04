# Todo List Application on GKE

This project demonstrates deploying a simple, basic Todo List application using Python, Flask, and MySQL on Google Kubernetes Engine (GKE). It showcases key cloud computing concepts such as containerization, orchestration, high availability, load balancing, and disaster recovery.

![Screenshot](Screenshot.png)

## Project Structure

```graphql
/todo-list-app
│
├── backend
│ ├── app.py                     # Flask application
│ ├── requirements.txt           # Python dependencies
│ └── init.sql                   # MySQL initialization script
│
├── frontend
│ ├── index.html                 # Frontend HTML
│ ├── script.js                  # Frontend JavaScript
│ └── style.css                  # Frontend CSS
│
├── k8s
│ ├── mysql-pvc.yaml            # claim persistent volume for mysql (both options)
│ ├── todo-app-deployment.yaml  # deploy flask+nginx+mysql containers (option 2)
│ ├── todo-app-pod.yaml         # pod with flask+nginx+mysql containers (option 1)
│ └── todo-app-service.yaml     # Service for flask+nginx+mysql app (option 1)
│
├── Dockerfile                  # Dockerfile for Flask app
├── nginx.conf                  # nginx configurations for reverse proxy
└── README.md
```

## Prerequisites

- Google Cloud Platform (GCP) account
- Google Cloud SDK installed and configured
- Docker installed for local development and containerization
- kubectl installed for interacting with the Kubernetes cluster

## Setup and Deployment

### Setup (before either option)

#### **Don't forget to replace `<YOUR_PROJECT_ID>` in the pod yamls and the shell commands**

```sh
# Enable APIs
gcloud services enable container.googleapis.com
gcloud services enable sqladmin.googleapis.com

# Create Cluser
gcloud container clusters create todo-list-cluster --num-nodes=1 --zone=us-central1-a
gcloud container clusters get-credentials todo-list-cluster --zone=us-central1-a

# clone repo
git clone https://github.com/fwSara95h/todo-list-flask.git
cd todo-list-flask

# REPLACE <YOUR_PROJECT_ID> IN THE YAML FILES AND ALSO IN THE COMMANDS BELOW

# Dockerize
gcloud auth configure-docker
docker build -t gcr.io/<YOUR_PROJECT_ID>/todo-backend .
docker push gcr.io/<YOUR_PROJECT_ID>/todo-backend

# ConfigMaps for SQL initialization and Nginx configuration
kubectl create configmap mysql-init-db-config --from-file=./database/init.sql
kubectl create configmap nginx-config --from-file=nginx.conf
kubectl create configmap nginx-html-config --from-file=./frontend/index.html --from-file=./frontend/script.js --from-file=./frontend/style.css

# Claim persistent volume for mysql
kubectl apply -f k8s/mysql-pvc.yaml 
```

### Create Port and Expose NodePort (Option 1)

```sh
kubectl apply -f k8s/todo-app-pod.yaml
# WAIT UNTIL POD IS READY - it might take a minute or so - use `kubectl get pods` to check that all 3 containers are ready
kubectl apply -f k8s/todo-app-service.yaml
```

Use `kubectl get nodes -o wide` to see external IP of node, and then go to **NODE-IP:30007**.

### Deploy and Expose LoadBalancer (Option 2)

```sh
kubectl apply -f k8s/todo-app-deployment.yaml
# WAIT UNTIL POD IS READY - it might take a minute or so - use `kubectl get pods` to check that all 3 containers are ready
kubectl expose deployment todo-app-deployment --type=LoadBalancer --name=todo-app-service --port=80 --target-port=80
# try setting target-port=5000 (to expose the flask container) if it just shows the nginx welcome page

# To view external IP (might have to wait a few minutes)
kubectl get services
```

## High Availability and Disaster Recovery
- This project includes configurations for a primary and a disaster recovery (DR) site using GKE.
- High availability is achieved through multiple replicas and load balancing.
- For disaster recovery, a secondary GKE cluster can be set up in a different region. Manual or automated failover strategies should be implemented based on the project requirements.


----

### OTHER NOTES for debugging etc

mysql client (copy podname after `kubectl get pods`):
```sh
kubectl exec -it pod/<POD-NAME> -c mysql --  mysql -u root -p
```
