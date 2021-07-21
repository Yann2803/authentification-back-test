User Manager API
Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites
MongoDB
User Manager API works with mongodb and you need to install it.
Download the MongoDB .tar.gz tarball on mongodb website.

Extract the files from the downloaded archive.

tar -zxvf mongodb-osx-ssl-x86_64-4.0.6.tgz

Create the data directory where you want store database.

mkdir -p ./data/db

Run MongoDB.

mongod --port 27017 --dbpath ./data/db

Begin using MongoDB.

mongo

Create database.

use newDB

db.user.insert({user_name: "admin", password: '' , email: 'admin@amin.com' , role: 'Admin' , authorization: null, "isUpdate" : false })
