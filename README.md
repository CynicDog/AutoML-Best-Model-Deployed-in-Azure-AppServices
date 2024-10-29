# AutoML-Best-Model-Deployed-in-Azure-AppServices

### Version Table
|                            | **Details**        |
|----------------------------|--------------------|
| Python                     | Python 3.9.20      |
| Conda                      | conda 24.7.1       | 

### Environment Variables 
- `BEST_MODEL_NAME`: `wheat_brake_11f3294kdb`
- `WS_NAME`: `inbrein-azure-ml-research-eunsang`
- `RG_NAME`: `inbrein-azure-ml-research`

## Steps 

### Download Best Model 

```powershell
PS C> az ml job download --name $BEST_MODEL_NAME `
        --all --download-path /app/configs/downloaded_artifacts `
        --workspace-name $WS_NAME `
        --resource-group $RG_NAME 
```

### Update Conda 
```powershell
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda update conda
Channels:
 - defaults
Platform: win-64
Collecting package metadata (repodata.json): done
Solving environment: done

# All requested packages already installed.
```

### Setup Conda Environment 

```powershell
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda init 
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda create -n automml python=3.9.20
(base) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> conda activate automml
(automml) PS C:\app\configs\downloaded_artifacts\named-outputs\best_model> pip install -r .\requirements.txt
```

### Setup Python Interpreter on PyCharm IDE 
<img width="100%" alt="image" src="https://github.com/user-attachments/assets/5b87323d-a745-4a68-8a3d-afbc7b7b48bd">

### Run the Server Locally 
```powershell
PS C:\Users> http POST http://localhost:8000/predict data:='[ [5.1,3.5,1.4,0.2], [7.0,3.2,4.7,1.4], [7.9,3.8,6.4,2.0], [6.9,3.1,4.9,1.5] ]'
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
