#!/bin/bash

function install_remote() {
    echo "installing remote (requires GIT)"
    mkdir -p $install_path
    pushd $install_path
    git clone git@github.com:Jstith/MarCANex.git
    pip3 install -r MarCANex/requirements-beacon.txt
    
    key=$(python3 -c 'from cryptography.fernet import Fernet; key = Fernet.generate_key(); print(key.decode())')
    echo $key > $install_path/MarCANex/C-2PO/beacon/sym.key
    
    chmod +x $install_path/MarCANex/C-2PO/beacon/beacon.py
    sudo ln -sf $install_path/MarCANex/C-2PO/beacon/beacon.py /usr/bin/c2po-beacon
    echo "Done! To start the beacon run \"c2po-beacon\""
    popd
    exit 0
}

function install_local() {
    echo "installing locally, requires zip file of directories"
    mkdir -p $install_path
}


read -p "Install target [full path] " install_path
read -n1 -p "Remote install (git) or local install? [r,l] " install_candidate
echo ""
case $install_candidate in
    r|R) install_remote ;;
    l|L) install_local ;;
    *) echo "Invalid input, exiting..." ; exit 1;
esac
