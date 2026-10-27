param([string]$baseDir = ".")
Set-Location $baseDir

$fpFiles = @()
if (Test-Path "face paint") {
    $fpFiles = @(Get-ChildItem -Path "face paint" -File | Where-Object { $_.Extension -match '\.(jpg|jpeg|png|webp|gif)$' } | Select-Object -ExpandProperty Name)
}

$mhFiles = @()
if (Test-Path "mehendi") {
    $mhFiles = @(Get-ChildItem -Path "mehendi" -File | Where-Object { $_.Extension -match '\.(jpg|jpeg|png|webp|gif)$' } | Select-Object -ExpandProperty Name)
}

$data = [PSCustomObject]@{
    facePaint = $fpFiles
    mehendi = $mhFiles
}

$json = $data | ConvertTo-Json -Depth 4
$jsContent = "// Auto-generated gallery images list`nconst GALLERY_IMAGES = " + $json + ";`n"
Set-Content -Path "gallery-data.js" -Value $jsContent -Encoding UTF8
Write-Host "Updated gallery-data.js successfully! Face Paint: $($fpFiles.Count) images, Mehendi: $($mhFiles.Count) images."
