# HLA_db
HLA database project for Tissue Typing. The project consists of a Django web application that links to a mysql (mariadb) database. The database stores HLA-typing output, provided in the form of .xlsx files. The application has an import function for adding new runs, and seach functions to display results according to relevant locus or variant allele.

# Installation
Dependencies can be found in the requirement.txt file. Pip installing these packages should ensure your HLA-db instance will work as intended. You will also need to initiate a mysql database named 'hla' and adjust the credentials as needed in the settings.py file.

The application has been tested on Ubuntu 20.04.4

# Usage

Assuming the mysql database is active, start the application by running 'python3 manage.py runserver 0.0.0.0:8000' from within the app directory (IP host may be changed if necessary).

In a browser, navigate to 0.0.0.0:8000 (or other IP address if changed) where you should see a page prompting you to log in. New users may be added by the system administrator using the admin interface (0.0.0.0:8000/admin). N.B. the administrator account must first be created using manage.py createsuperuser.

There are two main pages on the website, one is the homepage where searches can be undertaken, with the data displayed in the table at the bottom, and the other is the import data page, where new NGS runs can be added one at a time. If multiple runs are required to be added, it is best to ask the administrator to do a bulk upload using the seedFromExcel.py script.

IMPORTANT: the upload process may take up to a few minutes and there is currently no progress bar to indicate that it is working. Please be patient and wait to be redirected to either a 'Success' or 'Failure' page.

# Expected file format

Uploads are expected to be .xlsx NGS output, with at least a Summary tab and a Results tab. The latter tab may be named 'Transfer A & B', or anything else, but must be the last tab. The results tab must be in the format below:

Name	Component	Result
100755540	HLA-A*1	24:02
100755540	HLA-A*2	68:01
100755540	HLA-B*1	27:05
100755540	HLA-B*2	X
100755540	HLA-C*1	01:02
100755540	HLA-C*2	02:02
![image](https://user-images.githubusercontent.com/34276603/163376870-4a099dbb-6282-4f60-b060-ff195688f96c.png)

# How to get help

If you encounter any issues with the application please raise an issue at https://github.com/eastgenomics/HLA_db/issues or a ticket on the bioinformatics helpdesk (CUH only).
