# AutoML-Best-Model-Deployed-in-Azure-AppServices

### Version Table
| **         **              | **Details**        |
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

