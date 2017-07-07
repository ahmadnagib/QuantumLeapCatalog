# QuantumLeap Catalog

QuantumLeap (QL) is a catalog that provides a list of items within a variety of categories. QL allows users to add new categories and items to the catalog. QL provides user registration and authentication using OAuth.

This project is part of Udacity's Full Stack Web Developer Nanodegree Program. The login and authentication functionality is mainly inspired from Udacity's 'Authentication and Authorization' course lessons.

# Documentation

The information related to supported functionalities and how to get started is included in this documentation.

- [Supported Functionalities](#supported-functionalities)
- [Quick Start](#quick-start)
- [What is included](#what-is-included)
- [License](#license)


## Supported Functionalities

QuantumLeap supports Google+ authentication for using the catalog. A user have to be logged-in to enjoy the full functionalities of the QL catalog.

A logged-in user can:
- Add a new category/item
- Edit her/his own existing category(ies)/item(s)
- Delete her/his own existing category(ies)/item(s)

All the available categories and items are exposed in JSON format.

Kindly report any malfunctions by sending an email to [me](mailto:ahmadnagib@fci-cu.edu.eg).

## Quick start

### Local Deployment Software Prerequisites 

- [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) should be installed.
- It is recommended to use [Git Bash](https://git-for-windows.github.io/) or any similar BASH emulation if you are using Windows OS.
- [Udacity Fullstack Nanodegree Virtual Machine](https://github.com/udacity/fullstack-nanodegree-vm) should be downloaded or cloned.
- After running the VM (more details below), make sure that:
    - 'requests' module is installed using `sudo pip install requests` command.
    - 'werkzeug' version 0.8.3 is installed using `sudo pip install werkzeug==0.8.3` command.
    - 'flask' version 0.9 is installed using `sudo pip install flask==0.9` command.
    - 'Flask-Login' version 0.1.3 is installed using `sudo pip install Flask-Login==0.1.3` command.

### Deploy QuantumLeap Catalog Locally
1. Download [Udacity Fullstack Nanodegree Virtual Machine](https://github.com/udacity/fullstack-nanodegree-vm).
2. Download the [project's files](https://github.com/ahmadnagib/QuantumLeapCatalog) and put them altogether in 'catalog' folder of the VM.
3. Using Git Bash, move to the path of vagrant folder in the downloaded vm files.
4. Launch the Vagrant VM using `vagrant up` command (This might take a while in the first time).
5. Run `vagrant ssh` command to access the VM.
6. Move to 'catalog' folder containing the project files using `cd /vagrant/catalog`.
7. Run the QL Catalog application using `python ql-catalog.py`. 
8. This will make the Catalog available at [local host](http://localhost:5000).


The catalog app process running on the port can always be killed by using `fuser -k 5000/tcp` command.


## What is included

Within the downloaded folder you will find the following files:

```
quantumleapcatalog-master/
├──  models/
    ├── __init_.py
    ├── base.py
    ├── category.py
    ├── item.py
    ├── user.py
├──  views/
    ├── static/
        ├── main.css
    ├── templates/
        ├── addcategory.html
        ├── additem.html
        ├── allcategories_public.html
        ├── base.html
        ├── category.html
        ├── category_public.html
        ├── categoryitems_public.html
        ├── deletecategory.html
        ├── deleteitem.html
        ├── editcategory.html
        ├── edititem.html
        ├── item.html
        ├── item_public.html
        ├── login.html
    ├── app.py
    ├── categoryitems.py
    ├── databasesession.py
    ├── deletecategory.py
    ├── deleteitem.py
    ├── editcategory.py
    ├── edititem.py
    ├── getcategories.py
    ├── getcategory.py
    ├── getitem.py
    ├── login.py
    ├── logout.py
    ├── newcategory.py
    ├── newitem.py
    ├── utils.py
├── LICENSE
├── qlcatalog.py
├── README.md
├── README.md
├── secrets_of_g_client.json
```

## License

QuantumLeap Catalog is Copyright © 2017 Ahmad Nagib. It is free software, and may be redistributed under the terms specified in the [LICENSE](/LICENSE) file.
