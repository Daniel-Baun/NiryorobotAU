# User installation guide
### **Odoo installation**
Go to [Odoo download](https://www.odoo.com/documentation/16.0/administration/install/install.html) <br>
Follow the installation guide on the site, from the section **Source install**
Skip the part regarding Odoo Community installation<br>
Use the following command to initiate odoo<br> ```python3 odoo-bin --without-demo=all -d {database name}```

<br>
In the end the follwing things should be installed:
-pip
-PostgreSQL
-Odoo


### **Network settings**
To ensure the robots in your setup have static ip adresses, you need to enable some settings in the linux options.
Follow this guide, and use the Niryo manual to see how it can be changed.
[Static IP]()

### **PostgreSQL**
Download [pgAdmin](https://www.pgadmin.org/download/pgadmin-4-apt/) for PostgreSQL

### **Java**
Install java for Maestro to run
http://localhost/pgadmin4/browser