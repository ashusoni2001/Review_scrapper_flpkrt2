from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

_app = Flask(__name__)


@_app.route("/", methods=['GET'])
@cross_origin()
def Open_HomePage():
    return render_template("index.html")


@_app.route("/Reviews", methods=['POST'])
@cross_origin()
def Scrap_reviwes():
    if request.method == "POST":
        try:
            searched_item = str(request.form['content']).replace(" ", "")
            baseUrl = "https://www.flipkart.com/"
            prod_web_page = baseUrl + "search?q=" + searched_item
            req_page = uReq(prod_web_page)
            prod_page = req_page.read()
            prod_page_BS = bs(prod_page, "html.parser")
            prod_containers = prod_page_BS.find_all("div", {"class": "_1AtVbE col-12-12"})
            del prod_containers[0:2]
            _1st_prod = prod_containers[0]
            _1st_prod_link = str(baseUrl + "search?q=" + _1st_prod.div.div.div.a['href'])
            _1st_prod_link_req = uReq(_1st_prod_link)
            _1stPrdPage = _1st_prod_link_req.read()
            frstprdBS = bs(_1stPrdPage, "html.parser")

            filename = searched_item + ".csv"
            headers = "Product Name, Customer Name, Rating, Comment \n"
            with open(filename, 'w') as f:
                f.write(headers)
            comment_container = frstprdBS.find_all("div", {"class": "col _2wzgFH"})
            flpkr_reviews = []
            for i in comment_container:

                try:
                    prod_name = prod_page_BS.find_all('div', {'class': '_4rR01T'})[0].text
                except:
                    prod_name = 'Product Name Not Available'

                try:
                    # name=i.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    name = i.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                    print(name)

                except:
                    name = "haw! ja ko to naam hi mow ae"

                try:
                    rating = i.find_all("div", {"class": "_3LWZlK _1BLPMq"})[0].text
                    print(rating)
                except:
                    rating = "there is no rating"

                try:
                    comment = i.find_all("div", {"class": "t-ZTKy"})[0].text
                    print(comment)
                except:
                    comment = "No Comment aa thuu!"

                try :
                    values = f"{prod_name},{name},{rating}, {comment} \n"
                    with open(filename, 'a') as file:
                        file.write(values)
                except Exception as e:
                    print("An Exception has occured: ", e)

                review_dict = {'Product Name': prod_name, 'Customer Names': name, 'Ratings': rating, 'Comments': comment}
                flpkr_reviews.append(review_dict)

            return render_template("result.html", reviews=flpkr_reviews[0:(len(flpkr_reviews) - 1)])
        except Exception as e:
            print("An Exception has occured: ", e)
            return "Something is Wrong"

    else:
        render_template("index.html")


if __name__ == "__main__":
    _app.run(debug=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _app.run(debug=True, host="localhost")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
