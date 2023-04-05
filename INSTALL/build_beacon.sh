#!/bin/bash

function install_remote() {
    echo "installing remote (requires GIT)"
    mkdir -p $install_path
    git clone git@github.com:Jstith/MarCANex.git $install_path
    pip3 install -r $install_path/MarCANex/requirements-beacon.txt
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