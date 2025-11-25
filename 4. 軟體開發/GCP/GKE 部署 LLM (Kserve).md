## 1. 部署GKE

```bash
gcloud container clusters create sam-llm-test-cluster \
    --zone asia-east1-a \
    --machine-type n1-highmem-8 \
    --accelerator type=nvidia-tesla-t4,count=1 \
    --num-nodes 2
```

```bash
gcloud container clusters get-credentials sam-llm-test-cluster --zone asia-east1-a

```

## 2. 安裝 Kserve
```bash
# Knative 和 KServe 安裝
# Apply Knative Serving CRDs
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-crds.yaml

# Apply Knative Serving Core
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-core.yaml

# Wait for Knative Serving components to be ready
kubectl wait --for=condition=available --timeout=600s deployment/controller -n knative-serving
kubectl wait --for=condition=available --timeout=600s deployment/webhook -n knative-serving

# Apply Istio
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.15.1/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.15.1/net-istio.yaml

# Wait until Istio resources are ready
kubectl wait --for=condition=available --timeout=600s deployment/istio-ingressgateway -n istio-system
kubectl wait --for=condition=available --timeout=600s deployment/istiod -n istio-system

# Scale down Istio components
kubectl scale deployment istio-ingressgateway --replicas=1 -n istio-system
kubectl scale deployment istiod --replicas=1 -n istio-system

# Verify that Ingress Gateway service is available
kubectl --namespace istio-system get service istio-ingressgateway

# Apply Knative default configurations
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-default-domain.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-hpa.yaml

# Apply Cert-Manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.0/cert-manager.yaml

# Wait for Cert-Manager components to be ready
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager -n cert-manager
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager-webhook -n cert-manager
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager-cainjector -n cert-manager

# Apply KServe
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml

# Wait for KServe components to be ready
kubectl wait --for=condition=available --timeout=600s deployment/kserve-controller-manager -n kserve
kubectl wait --for=condition=available --timeout=600s deployment/kserve-webhook-server -n kserve

# Apply KServe Built-in ClusterServingRuntime
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve-cluster-resources.yaml

echo "All resources have been applied successfully!"

```


驗證安裝
```bash
kubectl get pods -n knative-serving

```
## 3. 部署LLM

創建命名空間
```bash
kubectl create namespace sam-llm-test-namespace
```

可以看資源
```bash
kubectl describe nodes | grep -E "nvidia.com/gpu|memory"

```

更新 kserve-huggingfaceserver
```bash
cat <<EOF > updated-huggingface-runtime.yaml
apiVersion: serving.kserve.io/v1alpha1
kind: ClusterServingRuntime
metadata:
  name: kserve-huggingfaceserver
spec:
  annotations:
    prometheus.kserve.io/path: /metrics
    prometheus.kserve.io/port: "8080"
  containers:
  - args:
    - --model_name={{.Name}}
    image: kserve/huggingfaceserver:latest-gpu
    name: kserve-container
    resources:
      limits:
        cpu: "1"
        memory: 2Gi
        nvidia.com/gpu: "1"
      requests:
        cpu: "1"
        memory: 2Gi
        nvidia.com/gpu: "1"
  protocolVersions:
  - v2
  - v1
  supportedModelFormats:
  - autoSelect: true
    name: huggingface
    priority: 1
    version: "1"
EOF

```

```bash
kubectl apply -f updated-huggingface-runtime.yaml

```

如果成功會看到
```
clusterservingruntime.serving.kserve.io/kserve-huggingfaceserver configured

```



sam-llm-test-llama.yaml
```bash

cat <<EOF > sam-llm-test-llama.yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sam-llm-test-llama
  namespace: sam-llm-test-namespace
  annotations:
    autoscaling.knative.dev/target: "1"
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      args:
        - --model_name=Llama3.2-3B
        - --model_id=meta-llama/Llama-3.2-3B-Instruct
        - --rope_scaling={"type":"linear", "factor":32.0}
        - --task=auto
        - --force_download=True
        - --gpu_memory_utilization=0.8
        - --max_model_len=8192
      env:
        - name: HF_TOKEN
          value: ""
      resources:
        limits:
          cpu: "4"
          memory: 20Gi
          nvidia.com/gpu: "1"  # 減少 GPU 請求為 1
        requests:
          cpu: "4"
          memory: 20Gi
          nvidia.com/gpu: "1"  # 減少 GPU 請求為 1
    minReplicas: 1
EOF



```


部署模型
```bash
kubectl apply -f sam-llm-test-llama.yaml
```

驗證模型部署
```bash
kubectl get inferenceservices sam-llm-test-llama -n sam-llm-test-namespace
```

```bash
kubectl describe inferenceservice sam-llm-test-llama -n sam-llm-test-namespace
```
## 4. 測試連線
```bash
kubectl get InferenceService -n sam-llm-test-namespace

```

```bash
kubectl get inferenceservices sam-llm-test-qwen -n sam-llm-test-namespace
kubectl get pods -n sam-llm-test-namespace
kubectl get svc istio-ingressgateway -n istio-system

```

## 5. 刪除
```bash
kubectl delete inferenceservice sam-llm-test-llama -n sam-llm-test-namespace
```

```bash
kubectl delete namespace sam-llm-test-namespace
```
