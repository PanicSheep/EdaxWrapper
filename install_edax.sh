#!/bin/bash
sudo add-apt-repository -y universe
sudo apt -y update
sudo apt -y install curl unzip g++ make p7zip-full

curl -OL https://github.com/abulmo/edax-reversi/archive/refs/tags/v4.4.zip
unzip v4.4.zip

pushd edax-reversi-4.4
	mkdir -p bin
	
	pushd src
		make build COMP=g++ BUILD=optimize ARCH=x64-modern
	popd
	
	pushd bin
		curl -OL https://github.com/abulmo/edax-reversi/releases/download/v4.4/eval.7z
		7z x eval.7z
	popd
popd