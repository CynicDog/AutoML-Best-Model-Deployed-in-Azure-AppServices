# AutoML-Pretrained-Model-Deployed-in-Azure-AppServices

### Index 
1. [A. Run the Server in Local Python Environment](#a-run-the-server-in-local-python-environment)
2. [B. Run the Server in a Local Docker Container](#b-run-the-server-in-a-local-docker-container)
3. [C. Run the Container as Azure WebApp](#c-run-the-container-as-azure-webapp)
4. [D. Run the Container as Azure Function App (Serverless)](#d-run-the-container-as-azure-function-app-serverless)

### Version Table
|                            | **Details**        |
|----------------------------|--------------------|
| Python                     | Python 3.9.20      |
| Conda                      | conda 24.7.1       | 

### 🌎 Local Development Environment Setup  

#### Download Best Model 

```powershell
PS C> az ml job download --name $BEST_MODEL_NAME `
        --all --download-path /app/configs/downloaded_artifacts `
        --workspace-name $WS_NAME `
        --resource-group $RG_NAME 
```

#### Update Conda 
```powershell
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda update conda
Channels:
 - defaults
Platform: win-64
Collecting package metadata (repodata.json): done
Solving environment: done

# All requested packages already installed.
```

#### Setup Conda Environment 

```powershell
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda init 
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda create -n automml python=3.9.20
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda activate automml
(automml) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> pip install -r .\requirements.txt
```

<details><summary><h4>Setup Python Interpreter on PyCharm IDE (Optional)</h4></summary>
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/5b87323d-a745-4a68-8a3d-afbc7b7b48bd">        
</details>

### 👩🏼‍🚀 Run the Flask Server  

## A. Run the Server in Local Python Environment 

#### 1. Run the flask server.
```powershell
(automml) PS C:\Users> python main.py 
```

#### 2. Test the functionality.
```powershell
(automml) PS C:\Users> http POST http://localhost:8000/predict data:='[ [5.1,3.5,1.4,0.2], [7.0,3.2,4.7,1.4], [7.9,3.8,6.4,2.0], [6.9,3.1,4.9,1.5] ]'
Connection: close
Content-Length: 85
Content-Type: application/json
Date: Tue, 29 Oct 2024 00:28:25 GMT
Server: Werkzeug/3.0.4 Python/3.9.20

{
    "predictions": [
        "Iris-setosa",
        "Iris-versicolor",
        "Iris-virginica",
        "Iris-versicolor"
    ]
}
```

## B. Run the Server in a Local Docker Container

#### 1. Pull the image. 
```powerhsell 
PS C:\Users> docker pull ghcr.io/cynicdog/automl-best-model-deployed-in-azure-appservices/automl-flask:latest
```

#### 2. Run the container.
```
PS C:\Users> docker run -p 8000:8000 ghcr.io/cynicdog/automl-best-model-deployed-in-azure-appservices/automl-flask:latest
```

#### 3. Test the functionality.
```powershell
(automml) PS C:\Users> http POST http://localhost:8000/predict data:='[ [5.1,3.5,1.4,0.2], [7.0,3.2,4.7,1.4], [7.9,3.8,6.4,2.0], [6.9,3.1,4.9,1.5] ]'
Connection: close
Content-Length: 85
Content-Type: application/json
Date: Tue, 29 Oct 2024 00:28:25 GMT
Server: Werkzeug/3.0.4 Python/3.9.20

{
    "predictions": [
        "Iris-setosa",
        "Iris-versicolor",
        "Iris-virginica",
        "Iris-versicolor"
    ]
}
```

## C. Run the Container as Azure WebApp   

#### 1. Create a dedicated Service Principal for the deployment.
```powershell
az ad sp create-for-rbac --name "automl-in-webapp" `
     --role Owner `
     --scopes /subscriptions/{SUBSCRIPTION_ID} `
     --sdk-auth
```
> This will return a JSON response with details about the created service principal. Save this JSON response as the GitHub repository secret `AZURE_CREDENTIALS`. Also, register additional secrets like `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID` with their respective values.

#### 2. Build the image and push to Azure Container Registry (ACR) by running the workflow [image-build-and-push-for-web-app.yaml](https://github.com/CynicDog/AutoML-Pretrained-Model-Deployed-in-Azure-AppServices/blob/main/.github/workflows/image-build-and-push-for-web-app.yaml).

#### 3. Deploy the container on Azure App Service as a Web App.

You can deploy the container using either the Azure CLI or the Azure Portal.

<details><summary><h5>3-a. Deploy with Azure CLI.</h5></summary>

- Enable Admin user

  If enabled, you can use the registry name as username and admin user access key as password to docker login to your container registry.
  ```bash
    az acr update \
      --name ${{ env.ACR_NAME }} \
      --admin-enabled true
        
    az acr credential show \
      --name ${{ env.ACR_NAME }} \
      --resource-group ${{ env.RG_NAME }}
  ```
  > This will return a list of two passwords. Save the first password as a repository secret `AZURE_CONTAINER_REGISTRY_PASSWORD`. 
  
- Run [deploy-web-app.yaml](https://github.com/CynicDog/AutoML-Pretrained-Model-Deployed-in-Azure-AppServices/blob/main/.github/workflows/deploy-web-app.yaml) workflow to deploy the container as a Web App. 

</details>

<details><summary><h5>3-b. Deploy on Azure Portal GUI.</h5></summary>

- Enable Admin User
  <img width="100%" alt="image" src="https://github.com/user-attachments/assets/c51204a5-8ac7-4957-bb95-406c4e5f7c5b">
  > On Azure Container Registry repository for the project, navigate to `Access Keys` and enable the `Admin User` option. 

- Basic information
  <img width="100%" src="https://github.com/user-attachments/assets/98f57fc3-1119-49c7-9ac2-a2867963006d">
  > Navigate to Azure AppServices and create a new instance. and  On `publish` option, make sure you select `Container`. Fill in other basic information on your need.

- Container information
  <img width="100%" src="https://github.com/user-attachments/assets/3edc25f0-e0ae-4634-b22a-23c4fa253df6">
  > Select the image previously pushed to ACR. If you don’t need additional networking or monitoring configurations, complete the creation process of the web app.
</details>

#### 4. Test the functionality. 
```powershell
PS C:\Users> http POST https://automl-webapp.azurewebsites.net/predict data:='[ [5.1,3.5,1.4,0.2], [7.0,3.2,4.7,1.4], [7.9,3.8,6.4,2.0], [6.9,3.1,4.9,1.5] ]'
HTTP/1.1 200 OK
Content-Length: 85
Content-Type: application/json
Date: Tue, 29 Oct 2024 05:49:09 GMT
Server: Werkzeug/3.0.6 Python/3.9.20

{
  "predictions": [
    "Iris-setosa",
    "Iris-versicolor",
    "Iris-virginica",
    "Iris-versicolor"
  ]
}
```
  
## D. Run the Container as Azure Function App (Serverless) 

#### 1. Create a dedicated Service Principal for the deployment.
```powershell
az ad sp create-for-rbac --name "automl-in-webapp" `
     --role Owner `
     --scopes /subscriptions/{SUBSCRIPTION_ID} `
     --sdk-auth
```
> This will return a JSON response with details about the created service principal. Save this JSON response as the GitHub repository secret `AZURE_CREDENTIALS`. Also, register additional secrets like `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID` with their respective values.

#### 2. Build the image for the container and deploy it on Azure Function App by runnning the workflow [deploy-function-app.yml](https://github.com/CynicDog/AutoML-Pretrained-Model-Deployed-in-Azure-AppServices/blob/main/.github/workflows/deploy-function-app.yml). 

#### 3. Test the functionality. 
```powershell
PS C:\Users> http POST https://automl-serverless.azurewebsites.net/predict data:='[ [5.1,3.5,1.4,0.2], [7.0,3.2,4.7,1.4], [7.9,3.8,6.4,2.0], [6.9,3.1,4.9,1.5] ]'
HTTP/1.1 200 OK
Content-Length: 85
Content-Type: application/json
Date: Thu, 31 Oct 2024 01:48:10 GMT
Server: Werkzeug/3.0.6 Python/3.9.20

{
    "predictions": [
        "Iris-setosa",
        "Iris-versicolor",
        "Iris-virginica",
        "Iris-versicolor"
    ]
}
```
