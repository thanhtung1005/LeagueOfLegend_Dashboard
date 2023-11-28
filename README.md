# **LeagueOfLegend_Dashboard**
A simple dashboard to manage "League of legend" database.
# **Installation**
## **Clone repository**
First, you need to download the repository. You can either run the script below on the command-line or terminal:

```
git clone https://github.com/thanhtung1005/LeagueOfLegend_Dashboard
```

## **Requirements:**
* Create environment by following command:
    ```console
    python -m venv env
    ```

* Activate environment:
    ```console
    env/Scripts/activate # For windows
    ```

* Install packages:
  ```console
  pip install -r requirements.txt
  ```

* You need to install MySQL to run this app (download [here](https://dev.mysql.com/doc/workbench/en/wb-installing-windows.html)). After doawnload you need to run `MySQL Workbench` and create a server with `username` and `password` to save database. Finally, change your `username` and `password` in file `.env` and `createDB.py`.

## **Run app**

* Create empty database at the first time run app:
    ```console
    python createDB.py
    ```
* Run app:
    ```console
    run.bat
    ```
* After run app, go to link http://127.0.0.1:100 to see dashboard

## **Features of dashboard**

- Import data
- Update data
- Delete data
- Add new data
