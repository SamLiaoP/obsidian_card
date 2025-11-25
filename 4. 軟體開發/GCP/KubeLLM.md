以下是一個 **更完整、包含「新增與修改檔案指令」** 的教學流程範本，讓你在 **GCP 上部署 KubeAI** 以及 **LLama3.2 3B** 模型，並且包含 **如何新增/修改檔案** 的示例命令。整個流程適用於 **Regional GKE Cluster** 並使用 **T4 GPU**。如有必要你可以將特定檔名、內容根據實際需求調整。

---

## **整體步驟總覽**

1. 建立並設定 GKE Cluster
2. 新增 GPU Node Pool (並鎖定到支援 T4 的子區域)
3. 安裝 KubeAI Controller (包含下載與修改 `values-gke.yaml`)
4. 新增並部署模型目錄 (`kubeai-models.yaml`)
5. 新增並部署 LLama3.2 3B 模型 (`llama3-3b.yaml`)
6. 測試模型 (OpenWebUI 與 Port-Forward 至 Jupyter Notebook)

---

## **步驟 1：建立並設定 GKE Cluster**

1. **更新 gcloud CLI**
    
    ```bash
    gcloud components update
    ```
    
2. **建立 Regional GKE Cluster**
    
    ```bash
    gcloud container clusters create kubeai-cluster \
        --region asia-east1 \
        --release-channel regular \
        --logging=SYSTEM,WORKLOAD \
        --monitoring=SYSTEM \
        --enable-autoscaling \
        --num-nodes=1 \
        --min-nodes=1 \
        --max-nodes=3
    ```
    
3. **連線到該集群**
    
    ```bash
    gcloud container clusters get-credentials kubeai-cluster --region asia-east1
    ```
    

---

## **步驟 2：新增 GPU Node Pool**

### **2.1 查詢支援 T4 的區域/zone**

```bash
gcloud compute accelerator-types list --filter="name:nvidia-tesla-t4"
```

假設我們確定 `asia-east1-a` 有支援 T4。

### **2.2 建立 GPU Node Pool**

```bash
gcloud container node-pools create gpu-pool \
    --cluster kubeai-cluster \
    --region asia-east1 \
    --node-locations=asia-east1-a \
    --accelerator type=nvidia-tesla-t4,count=1 \
    --machine-type n1-highmem-8 \
    --num-nodes=1 \
    --enable-autoscaling \
    --min-nodes=0 \
    --max-nodes=2 \
    --labels node-role=gpu \
    --preemptible
```

> _`--node-locations=asia-east1-a` 鎖定到有 T4 的子區域，`--preemptible` 表示可搶占節點，成本更低但可能會中斷。_

---

## **步驟 3：安裝 KubeAI Controller**

### **3.1 安裝 Helm 並加入 Repo (若尚未安裝 Helm)**

若你尚未在 Cloud Shell 安裝 Helm，可先安裝：

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

加入並更新 KubeAI Repository：

```bash
helm repo add kubeai https://substratusai.github.io/kubeai
helm repo update
```

### **3.2 下載並修改 `values-gke.yaml`**

1. **下載檔案**
    
    ```bash
    curl -L -O https://raw.githubusercontent.com/substratusai/kubeai/refs/heads/main/charts/kubeai/values-gke.yaml
    ```
    
2. **編輯檔案**  
    你可用任一文字編輯器（`nano`, `vi` 等）開啟並修改；以下以 `nano` 為例：
    
    ```bash
    nano values-gke.yaml
    ```
    
    在 `resourceProfiles` 區塊中，若沒有 T4 配置，可手動新增：
    
    ```yaml
    resourceProfiles:
      nvidia-gpu-t4:
        nodeSelector:
          cloud.google.com/gke-accelerator: "nvidia-tesla-t4"
          cloud.google.com/gke-spot: "true"
    ```
    
    編輯完按 `Ctrl+X`, `Y`, `Enter` 儲存退出。
    

### **3.3 部署 KubeAI Controller**

1. **設置 Hugging Face Token（若需要下載 HF 模型）**
    
    ```bash
    export HUGGING_FACE_HUB_TOKEN=[Your-HF-Access-Token]
    ```
    
2. **使用 Helm 部署**
    
    ```bash
    helm upgrade --install kubeai kubeai/kubeai \
        -f values-gke.yaml \
        --set secrets.huggingface.token=$HUGGING_FACE_HUB_TOKEN \
        --wait
    ```
    
3. **確認 Pods**
    
    ```bash
    kubectl get pods -n kubeai
    ```
    
    確認 `kubeai` 和 `openwebui` 等相關 Pod 已正確啟動。

---

## **步驟 4：新增並部署模型目錄 (`kubeai-models.yaml`)**

1. **新增檔案**  
    若要在 Shell 中一次完成檔案建立，可使用這種 `cat <<EOF` 語法：
    
```bash
cat <<EOF > kubeai-models.yaml
catalog:
  llama3-3b:
    enable: true
EOF
````

```bash
helm install kubeai-models kubeai/models -f kubeai-models.yaml
```


---

## **步驟 5：新增並部署 LLama3.2 3B 模型 (`llama3-3b.yaml`)**

1. **新增檔案**
    
```bash
cat <<EOF > llama3-3b.yaml
apiVersion: kubeai.org/v1
kind: Model
metadata:
  name: llama3-3b
spec:
  features: [TextGeneration]
  owner: openai
  url: ollama://llama3:3b
  engine: OLlama
  resourceProfile: nvidia-gpu-t4:1
  minReplicas: 0
  replicas: 1
EOF
````
> *`resourceProfile: nvidia-gpu-t4:1` 表示使用剛才在 `values-gke.yaml` 定義的 T4 profile 並分配 1 顆 GPU。*

2. **套用該模型檔案**  
```bash
kubectl apply -f llama3-3b.yaml
````

3. **檢查狀態**
    
    ```bash
    kubectl get model llama3-3b
    kubectl get pods
    ```
    
    確認模型對應的 Pod 順利啟動。

---

## **步驟 6：測試模型**

### **6.1 透過 OpenWebUI 測試**

1. **Port-Forward**
    
    ```bash
    kubectl port-forward svc/openwebui 8080:80
    ```
    
2. **在瀏覽器中打開**  
    `http://localhost:8080`  
    選擇 `llama3-3b` 進行交互測試。

### **6.2 讓 Jupyter Notebook 呼叫模型**

#### **6.2.1 Port-Forward 方式**

1. **開啟另一個終端**
    
    ```bash
    kubectl port-forward svc/kubeai 8080:80
    ```
    
2. **Notebook 內測試** (範例)
    
    ```python
    import requests
    
    url = "http://localhost:8080/v1/chat/completions"
    payload = {
        "model": "llama3-3b",
        "messages": [
            {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    ```
    

#### **6.2.2 若 Notebook 與 K8s 同網路 (Cluster IP)**

- 可以建立一個 `ClusterIP` or `LoadBalancer` Service 來讓 Notebook 直接用 `ClusterIP` / `LoadBalancer IP` 去存取。
- 例如，建立一個 `Service` 針對我們的模型 Pod Selector，也或直接存取 `svc/kubeai` 之 `ClusterIP`。

---

## **總結建議**

1. **Node Pool 自動擴縮**
    
    - 由於我們設定 `--min-nodes=0 --max-nodes=2`，在負載低的時候，GPU 節點可以自動縮容至 0，節省成本。
2. **Spot/Preemptible 節點**
    
    - 若對可搶占的中斷風險容忍度高，可用 `--preemptible` 節省更多費用。
3. **Scale 你的模型**
    
    - 用 `kubectl scale model/llama3-3b --replicas=2` 可快速擴充 Pod 副本數； 或 `--replicas=0` 完全關閉以節省 GPU。
4. **檢查 Logs 與 Metrics**
    
    - `kubectl logs` 及 `kubectl top pods/nodes` 監控使用率，確定部署健康度。

---

以上流程已包含 **如何新增與修改檔案** 的指令（使用 `nano` 或 `cat <<EOF > file.yaml`），以及 **如何在 Cloud Shell 進行操作**。照此步驟應能順利在 **GCP（Regional GKE + T4 GPU）** 上啟用 **KubeAI** 以及部署 **LLama3.2 3B** 模型，再透過 **Notebook** 呼叫。若有進一步疑問，歡迎再討論！