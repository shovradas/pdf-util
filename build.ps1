Write-Output "Build started ..."
Write-Output "==================================================================="


### build sdist and wheel ---------------------------------------------------------
poetry build 
### build sdist and wheel ends ----------------------------------------------------


### build self-contained distribution for windows ---------------------------------
$rootDir = $PSScriptRoot
$distDir = "$rootDir/dist"
$artifactsDir = "$rootDir/artifacts"

# Collect necessary file paths
$artifacts = @{
    getPip = "$artifactsDir/get-pip.py"
    python = "$artifactsDir/$((Get-ChildItem -Path $artifactsDir -Filter 'python-*.zip')[0].Name)"
    # python = "$artifactsDir/python-3.9.6-embed-amd64.zip"
}
$wheel = (Get-ChildItem -Path $distDir -Filter *.whl)[0]
$package, $version, $_ = $wheel.Name.Split("-" ,3)

# Define necessary paths
$outDir = "$distDir/$package-$version-windows-amd64"
$pythonDir = "$outDir/python"
$pythonExe = "$pythonDir/python.exe"
$libDir = "$outDir/lib"
$binDir = "$outDir/bin"

# Clean and create the output directory
if(Test-Path $outDir) { Remove-Item -Path $outDir -Recurse }
New-Item -ItemType "directory" -Path $outDir | Out-Null

# Adding python to the distribution
Expand-Archive -Path $artifacts.python -DestinationPath $pythonDir

# Adding necessary python path
$libDirRelative = [System.IO.Path]::GetRelativePath($pythonDir, $libDir)
$pythonPathFile = (Get-ChildItem -Path $pythonDir -Filter *._pth)[0].FullName
Add-Content $pythonPathFile "import site"
Add-Content $pythonPathFile $libDirRelative

# Install pip, wheel distribution and clean
Invoke-Expression "$pythonExe $($artifacts.getPip) --no-setuptools --no-wheel"
Invoke-Expression "$pythonExe -m pip install $wheel --target $libDir"
Invoke-Expression "$pythonExe -m pip uninstall -y pip"

# Clean lib/bin if any
$libBinDir = "$libDir/bin/"
if(Test-Path $libBinDir) { Remove-Item -Path $libBinDir -Recurse }

# Add run script
$pythonExeRelative = [System.IO.Path]::GetRelativePath($binDir, $pythonExe)
New-Item -ItemType "directory" -Path $binDir | Out-Null
Add-Content "$binDir/pdfutil.bat" "@echo off`n$pythonExeRelative -m pdfutil"
Add-Content "$binDir/pdfutil.ps1" "$pythonExeRelative -m pdfutil | Out-Null"

# Compress the distribution
$outDirZip = "$outDir.zip"
if(Test-Path $outDirZip) { Remove-Item -Path $outDirZip }
Compress-Archive -Path $outDir -DestinationPath $outDirZip

# Clean
Remove-Item -Path $outDir -Recurse
### build self-contained distribution for windows ends ---------------------------


Write-Output "==================================================================="
Write-Output "Build finished"