from threading import Thread
from libraries.alert import *
from libraries.file_management import *

def main():

    user_message = loadFileContent("message.txt")

    #initizalize urls and class names
    funda_url = "https://www.funda.nl/zoeken/huur?selected_area=%5B%22groningen%22%5D&price=%22900-1500%22&sort=%22date_down%22&search_result=1"
    funda_base_url = "https://www.funda.nl"
    funda_class_name = "text-blue-2 visited:text-purple-1 cursor-pointer"

    rotsvast_url = "https://www.rotsvast.nl/woningaanbod/?type=2&searchPattern=Gronin&office=0&minimumPrice[2]=700&maximumPrice[2]=1500"
    rotsvast_base_url = "https://www.rotsvast.nl"
    rotsvast_class_name = "clickable-block"

    househunting_url = "https://househunting.nl/en/housing-offer/?available-since=&interior=Gestoffeerd&type=for-rent&filter_location=Groningen&lat=53.2193835&lng=6.5665018&km=1&km=1&min-price=800&max-price=1500&vestiging=&sort="
    househunting_base_url = "https://househunting.nl"
    househunting_class_name = "location"

    etd_url = "https://www.123wonen.nl/huurwoningen/in/groningen/sort/newest"
    etd_base_url = "https://www.123wonen.nl"
    etd_wonen_class_name = "textlink-design orange"

    tuitman_url = "https://www.tuitmanvastgoedbeheer.nl/huuraanbod-Groningen-Drenthe-Zwolle-Vind-uw-huurwoning-bij-ons"
    tuitman_base_url = "https://www.tuitmanvastgoedbeheer.nl"
    tuitman_class_name = "ftReadMore"

    vdmeulen_url = "https://www.vandermeulenmakelaars.nl/en/objecten/?filter=1&gestoffeerd=1"
    vdmeulen_base_url = "www.vandermeulenmakelaars.nl"
    vdmeulen_class_name = "btn-default"

    pandomo_url = "https://www.pandomo.nl/huurwoningen/?filter-group-id=10&filter%5B39%5D=775%2C1475"
    pandomo_base_url = "https://www.pandomo.nl"
    pandomo_class_name = "results__item"

    bens_url = "https://www.bensverhuurenbeheer.nl/aanbod/prijs=between(800,1500)/status=beschikbaar"
    bens_base_url = "https://www.bensverhuurenbeheer.nl"
    bens_class_name = "module verhuur estate overview"
    # bens_class_name = "module estate_filter"
    # bens_class_name = "figure"


    #intitlaize old res for all sites
    print("Setting initial state for all websites. This might take a while.")
    funda_old_res = GetPageSource(funda_url, funda_class_name)
    rotsvast_old_res = GetPageSource(rotsvast_url, rotsvast_class_name)
    househunting_old_res = GetPageSource(househunting_url, househunting_class_name)
    etd_wonen_old_res = GetPageSource(etd_url, etd_wonen_class_name)
    tuitman_old_res = GetPageSource(tuitman_url, tuitman_class_name)
    vdmeulen_old_res = GetPageSource(vdmeulen_url, vdmeulen_class_name)   
    pandomo_old_res = GetPageSource(pandomo_url, pandomo_class_name)
    bens_old_res = GetPageSource(bens_url, bens_class_name)
    print("Inital set-up complete")

    #start the loop
    while True:
        funda_old_res = ParsePage(funda_url, funda_base_url, False, user_message, funda_old_res, funda_class_name, "a")
        rotsvast_old_res = ParsePage(rotsvast_url, rotsvast_base_url, False, user_message, rotsvast_old_res, rotsvast_class_name, "a")
        househunting_old_res = ParsePage(househunting_url, househunting_base_url, False, user_message, househunting_old_res, househunting_class_name, "li")
        etd_wonen_old_res = ParsePage(etd_url, etd_base_url, False, user_message, etd_wonen_old_res, etd_wonen_class_name, "a")
        tuitman_old_res = ParsePage(tuitman_url, tuitman_base_url, True,user_message, tuitman_old_res, tuitman_class_name, "a")
        vdmeulen_old_res = ParsePage(vdmeulen_url, vdmeulen_base_url, False, user_message, vdmeulen_old_res, vdmeulen_class_name, "a")
        pandomo_old_res = ParsePage(pandomo_url, pandomo_base_url, True, user_message, pandomo_old_res, pandomo_class_name, "li")
        bens_old_res = ParsePage(bens_url, bens_base_url, False, user_message, bens_old_res, bens_class_name, "a")

if __name__ == '__main__':
    main()

