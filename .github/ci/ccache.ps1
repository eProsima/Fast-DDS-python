$erroractionpreference = "stop"

$tag = (Invoke-WebRequest -Uri "https://api.github.com/repos/ccache/ccache/releases" -UseBasicParsing | ConvertFrom-Json)[0].tag_name
$name = (Invoke-WebRequest -Uri "https://api.github.com/repos/ccache/ccache/releases" -UseBasicParsing | ConvertFrom-Json)[0].name
$filename = "ccache-$name-windows-x86_64"
$tarball = "$filename.zip"

$outdir = $pwd.Path
$outdir = "$outdir\.github"
mkdir $outdir
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri "https://github.com/ccache/ccache/releases/download/$tag/$tarball" -OutFile "$outdir\$tarball"

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$outdir\$tarball", "$outdir")
Move-Item -Path "$outdir\$filename" -Destination "$outdir\ccache"
