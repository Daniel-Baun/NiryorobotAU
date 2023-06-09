# Bachelor thesis in Flexible Manufacturing into Digital Twins.
This repository serves as the codebase for the bachelor thesis in Flexible Manufacturing into Digital Twins<br>
The group members are:
- [Daniel Baun Olesen](https://github.com/Daniel-Baun)
- [Rasmus Maarssø Carlsen](https://github.com/Rasmus-M-C)
## User installation guide
### **Odoo installation**
Go to [Odoo download](https://www.odoo.com/documentation/16.0/administration/install/install.html) <br>
Follow the installation guide on the site, from the section **Source install**
Skip the part regarding Odoo Community installation<br>
Use the following command to initiate odoo<br> 
```
python3 odoo-bin --without-demo=all -d {database name}
```

<br>
In the end the following should be installed:

- pip
- PostgreSQL
- Odoo


### **Network settings**
To ensure the robots in your setup have static ip adresses, you need to enable some settings in the linux options.
Follow this guide, and use the Niryo manual to see how it can be changed.
[Static IP](https://www.tomshardware.com/how-to/static-ip-raspberry-pi )

### **PostgreSQL**
[Install](https://www.pgadmin.org/download/pgadmin-4-apt/) the web version of pgAdmin for PostgreSQL<br>
Run the command 
```
sudo /usr/pgadmin4/bin/setup-web.sh
```

Go to the pgadmin interface:<br> http://localhost/pgadmin4/browser <br>
To login to the interface using earlier created credentials<br>
Connect to the database using the this [guide](https://www.postgresqltutorial.com/postgresql-getting-started/connect-to-postgresql-database/) <br>
Run the following query <br>
```
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  desc_item CHAR(4) NOT NULL,
  no_product INTEGER NOT NULL,
  status VARCHAR NOT NULL,
  dateinserted DATE NOT NULL,
  failure_status BOOLEAN NOT NULL
);
```
In Odoo go to Inventory -> Products.
Click "New" and create 6 new products using the table below<br>
 1. Fill in "Product name"
 2. Fill in "Internal reference"
 3. Click "Update quantity" and type 50. <br>
 This is your product stock
 4. Click "New"
   ![alt text](https://github.com/Daniel-Baun/NiryorobotAU/blob/master/Figures/Screenshot%20from%202023-06-01%2013-25-58.png?raw=true)

| Product name    | Internal reference |
|-----------------|--------------------|
| Green Rectangle | GR01               |
| Green Circle    | GC01               |
| Red Rectangle   | RR01               |
| Red Circle      | RC01               |
| Blue Rectangle  | BR01               |
| Blue Circle     | BC01               |
|                 |                    |




### **UniFMU**
Install UniFMU using their [repository](https://github.com/INTO-CPS-Association/unifmu)

### **Maestro**
Install Maestro using their [repository](https://github.com/INTO-CPS-Association/maestro) <br>
Install [Java](https://www.java.com/en/download/help/linux_x64_install.html#download)  for running Maestro

### **RabbitMQFMU**
Install RabbitMQFMU using their [repository](https://github.com/INTO-CPS-Association/fmu-rabbitmq)
