# CodInGame Python Multi-file Script phyCharm

Minimally forked from https://github.com/devYaoYH/cg_pyEnv 

Simple script to collect python class definitions across multiple files with `build <file>`.

## Install

Download the package from github and run pip install **<folder where cg_pyEnv is located>**

## Sample Workflow
project structure:

codInGame:
     lib/
          your packages
          cg_pyEnv

     any_project/ # for example 'mars_lander'   
     

in project folder simply run build xxx.py
...or define a file watcher in your IDE 

## Issues

1. Generate dependency tree and resolve order of imports automatically
