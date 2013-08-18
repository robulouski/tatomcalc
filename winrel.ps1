#
# Trade-A-Tron-O-Matic Calc
# Windows build script
# 
# Wrapper script, sets up environment and runs pyinstaller to create
# binary package.
#
# Usage:
#  winrel.ps1 <product> <version> <run_script>
#

[CmdletBinding()]
Param(
  [Parameter(Mandatory=$True,Position=1)]
  [string]$PRODUCT,
  [Parameter(Mandatory=$True,Position=2)]
  [string]$VERSION,
  [Parameter(Mandatory=$True,Position=3)]
  [string]$RUN_SCRIPT
)

$RELEASE = $PRODUCT + "-" + $VERSION

$OUTDIR = "release/win/${VERSION}"
$DISTDIR = "$OUTDIR/dist/${PRODUCT}"
$PARENTDISTDIR = "$OUTDIR/dist/"
$ARCHIVE = "${PRODUCT}-${VERSION}-win.zip"

Write-Host "$PRODUCT version $VERSION"
Write-Host "Building Windows release $RELEASE"
Write-Host "Creating release in $OUTDIR"

workon pyside
python.exe C:\Install\pyinstaller2\pyinstaller.py -o $OUTDIR -n $PRODUCT -w $RUN_SCRIPT
$exists = test-Path $DISTDIR
if ($exists -eq $true) {
	Copy-Item README.md -destination $DISTDIR\README.TXT
	push-location $PARENTDISTDIR
	$archcmd = 'C:\Program Files\7-Zip\7z.exe' 
	& $archcmd a $ARCHIVE $PRODUCT\
	pop-location
}
