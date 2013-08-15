#!/bin/bash

if [ $# -lt 3 ]; then
	echo "Usage: $0 <product> <version> <run_script>"
	exit 1
fi

# Product name
PRODUCT=$1
VERSION=$2
RUNSCRIPT=$3

# Release identifier
RELEASE="${PRODUCT}-${VERSION}"

OUTDIR="release/linux/${VERSION}"
DISTDIR="$OUTDIR/dist/${PRODUCT}"
ARCHIVE="${PRODUCT}-${VERSION}-linux.tar.gz"
echo "$PRODUCT version $VERSION"
echo "Building Linux release $RELEASE"
echo "Creating release in $OUTDIR"

~/install/pyinstaller2/pyinstaller.py -o ${OUTDIR} -n ${PRODUCT} ${RUNSCRIPT}
if [ -d ${DISTDIR} ]; then
	cp README.md ${DISTDIR}
	tar czvf ${ARCHIVE} -C `dirname ${DISTDIR}` ${PRODUCT}/
fi
