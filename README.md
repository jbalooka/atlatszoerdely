# atlatszoerdely
Files for Data Mining and Management of atlatszoerdely projects


#Installation on Ubuntu
##Git Client
You need this to get the contents of this repository.  
```sh  
sudo apt-get update  
sudo apt-get install git  
```
##Java

Install OpenJDK. Java is needed for Neo4j.
```sh  
sudo apt-get install openjdk-9-jre 
```
##Neo4j
This is the Graph Database that will Store All of Our Data  
Follow the instructions as described here: https://www.digitalocean.com/community/tutorials/how-to-install-neo4j-on-an-ubuntu-vps#installing-neo4j  

Long Story Short: Neo4j Is not an official Ubuntu / Debian Package therefore you will have to add it's location to your computers repository paths. After it's done, make sure to refresh your Package Installer and then Install neo4j

##Python2.7 Interpreter
Python scripts will help us interpret massive amounts of data and move them to the Database  
Use a Precompiled Python Interpreter: 
```sh  
sudo add-apt-repository ppa:fkrull/deadsnakes  
sudo apt-get update  
sudo apt-get install python2.7  
```
###pip package installer for Python
This is a Package Manager for Python. It eases installing python packages a lot. The same idea as for Ubuntu package manager, in this case for a smaller system (Python only)
```sh  
sudo apt-get install python-pip 
```
###neo4j python connector
This is needed for Python to communicate with the neo4j DB
```sh 
pip install neo4j-driver
```

##OpenOffice
Editing and Viewing Datasets from Excel and / or Word Files. You can use LibreOffice as well as an alternative.  
```sh 
sudo apt-get libreoffice  
```
#Installation on Windows
Download the Installers and simply Execute them.


#Using the Contract Importer
##1. Checkout this Git Repository  
Create a folder that you will use as a Repo Dir
```sh  
mkdir ~/atlatszoerdely  
cd ~/atlatszoerdely  
git clone 
```
##2. Go to contract.py folder and start the import process
```sh  
cd ~/atlatszoerdely/lib/contracts
python contract.py -f "<full path of the csv file>" -o "<Name of the Organization>"
```
