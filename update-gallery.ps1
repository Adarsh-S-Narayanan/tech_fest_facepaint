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
$jsContent = "// Auto-generated gallery images list`nwindow.GALLERY_IMAGES = " + $json + ";`nvar GALLERY_IMAGES = window.GALLERY_IMAGES;`n"
Set-Content -Path "gallery-data.js" -Value $jsContent -Encoding UTF8
Write-Host "Updated gallery-data.js successfully! Face Paint: $($fpFiles.Count) images, Mehendi: $($mhFiles.Count) images."

# Auto-sync prices if prices.json exists
if (Test-Path "prices.json") {
    $pricesRaw = Get-Content "prices.json" -Raw
    $pricesJson = $pricesRaw | ConvertFrom-Json
    $flatMap = [ordered]@{}
    foreach ($prop in $pricesJson.PSObject.Properties) {
        if ($prop.Value -is [System.Management.Automation.PSCustomObject]) {
            foreach ($subProp in $prop.Value.PSObject.Properties) {
                if ($null -ne $subProp.Value) {
                    $flatMap[$subProp.Name.ToLower()] = $subProp.Value
                }
            }
        } elseif ($null -ne $prop.Value) {
            $flatMap[$prop.Name.ToLower()] = $prop.Value
        }
    }
    $priceMapJson = $flatMap | ConvertTo-Json
    $priceJsContent = "// Auto-generated prices list from prices.json`nwindow.PRICES_DATA = " + $pricesRaw.Trim() + ";`nwindow.PRICE_MAP = " + $priceMapJson + ";`n"
    Set-Content -Path "prices-data.js" -Value $priceJsContent -Encoding UTF8
    Write-Host "Updated prices-data.js with $($flatMap.Count) priced items."
}
