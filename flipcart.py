from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
from flask import Flask,request,jsonify

url="https://www.flipkart.com"
app=Flask(__name__)
@app.route("/",methods=["POST"])
def get():
    product=request.json.get("product")
    # ops = Options()
    # ops.add_argument("--headless")
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(product)
        search_box.submit()
        
        sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("a", class_="k7wcnx")
        res = []
        for i in products:
            try:
                proname = i.find("div",class_="RG5Slk") 
                proprize = i.find("div",class_="hZ3P6w") 
                proimg = i.find("img",class_="UCc1lI") 
                
                if proname and proprize and proimg:
                    res.append({
                        "name": proname.text.strip(),
                        "prize": proprize.text.strip(),
                        "img": proimg['src']
                    })
            except Exception as e:
                print(f"Skipping product due to error: {e}")
        
        with open("./data.json","w") as f:
            json.dump(res,f,indent=4)
        return jsonify(res)

    finally:
        driver.quit()
if __name__ == "__main__":
    app.run(debug=True)