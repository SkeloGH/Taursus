#!/bin/bash

# Check if ta-lib is already installed
if [ -d "/usr/local/lib/ta-lib" ]; then
  echo "ta-lib is already installed, skipping installation"
  exit 0
fi

# Check if a C compiler is already installed
if command -v gcc &> /dev/null; then
  echo "C compiler is already installed, skipping installation"
else
  echo "Installing GCC..."
  sudo apt-get update
  sudo apt-get install -y build-essential
fi

# Install Python3 development headers
sudo apt-get install libpython3-dev

 # prompt if user wants to reinstall
echo "Do you want to reinstall ta-lib? (y/n)"
read answer
if [ "$answer" == "y" ]; then
  # uninstall ta-lib
  sudo rm -rf /usr/local/lib/ta-lib
  sudo rm -rf /usr/local/include/ta-lib
  sudo rm -rf /usr/local/bin/ta-lib-config
fi

# Configure TA-Lib and make only if not already installed
if [ -d "/usr/local/lib/ta-lib" ]; then
  echo "ta-lib is already installed, skipping installation"
else
  # Download and extract the tarball
  if [ -f "ta-lib-0.4.0-src.tar.gz" ]; then
    echo "ta-lib tarball is already downloaded, skipping download"
  else
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
  fi

  if [ -d "ta-lib" ]; then
    echo "ta-lib is already extracted, skipping extraction"
  else
    tar -xzf ta-lib-0.4.0-src.tar.gz
  fi

  # Install TA-Lib
  echo "Installing ta-lib..."
  cd ta-lib
  ./configure --prefix=/usr/local
  make
  sudo make install
  cd ..
  rm -rf ta-lib
  rm ta-lib-0.4.0-src.tar.gz

fi
