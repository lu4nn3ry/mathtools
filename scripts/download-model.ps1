# Download Qwen 2.5 7B Instruct (GGUF) for local LLM explanations
# Requires: curl or Invoke-WebRequest

$modelDir = Join-Path $PSScriptRoot ".." "models" "qwen"
$modelUrl = "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf"
$modelFile = Join-Path $modelDir "qwen2.5-7b-instruct-q4_k_m.gguf"

New-Item -ItemType Directory -Path $modelDir -Force | Out-Null

if (Test-Path $modelFile) {
    Write-Host "Model already exists at $modelFile"
    exit 0
}

Write-Host "Downloading Qwen 2.5 7B Instruct (Q4_K_M, ~4.5 GB)..."
Write-Host "URL: $modelUrl"
Write-Host "Destination: $modelFile"
Write-Host ""

try {
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile($modelUrl, $modelFile)
    Write-Host "Download complete!"
} catch {
    Write-Host "Download failed: $_"
    Write-Host "Try manually downloading from:"
    Write-Host $modelUrl
    exit 1
}
