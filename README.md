# Django_Bookshelf_App

<strong>Description</strong>

<p> Book Store web application where user with sufficient credentials can access, store & manage their favourite books 
in different sections such as custom <strong>tags/recents/favourites</strong> etc. It also provides a <strong>search</strong> functionality to find 
books of choice easily.It uses the browser's in-built pdf reader to read the books and user can also download them 
to disk. Multiple users can concurrently use the web application to access their books without any performance issue. </p>

<strong>Features</strong>

<p>
1. Authentication <br>
2. Store books on cloud and access from any device,anywhere <br>
3. Manage books according to tags (specified by user), recents and your favourite books (your fav. books are detected automatically by website) <br>
4. Search books by tags, name of book, author of book etc. <br>
5. Download books on your device. <br>
6. Share books (you can give access to your books to another user) <br>
</p>

<strong>Run the following commands to setup and run it on your local host:</strong>

<strong>Setup on Linux</strong>

first switch to the directory where you want to store it,then open terminal and run the following commands - 

<strong>
git clone https://github.com/gagangarg631/Django_Bookshelf_App

cd Django_Bookshelf_App <br>
sudo apt install python3 <br>

sudo pip3 install virtualenv <br>
virtualenv new_virtual_env_name <br>
source new_virtual_env_name/bin/activate <br>

pip install -r requirements.txt <br>
python manage.py runserver <br>
</strong>

then copy & paste the url shown in the terminal in your browser


<strong>Setup on Windows (most of the work is same as linux)</strong>

first switch to the directory where you want to store it,then open cmd and run the following commands - 

<strong>
git clone https://github.com/gagangarg631/Django_Bookshelf_App

cd Django_Bookshelf_App <br>
download and install python in your pc and set to path and open cmd
  
pip install virtualenv <br>
virtualenv new_virtual_env_name <br>
new_virtual_env_name\Scripts\activate <br>

pip install -r requirements.txt <br>
python manage.py runserver <br>
</strong>

then copy & paste the url shown in the cmd in your browser

