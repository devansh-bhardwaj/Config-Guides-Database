from driver import driver
from selenium.webdriver.common.by import By

black_listed =  ['http://www.cisco.com/c/en/us/td/docs/general/whatsnew/whatsnew.html', 'http://www.cisco.com/go/cfn', 'https://cfnng.cisco.com/', 'https://tools.cisco.com/Support/CLILookup', 'https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mcl/allreleasemcl/all-book.html', 'http://www.cisco.com/go/mibs', 'https://www.cisco.com/c/en/us/support/index.html']

def search_page(link, landing_links):
    try:
        if link != None: driver.get(link)
    except:
        pass
    further_links = []
    try:
        page_search_area = driver.find_element(By.ID, "pageContentDiv")
        psa = page_search_area.find_elements(By.TAG_NAME, "a")
        for lin in psa:
            lnk = lin.get_attribute("href")
            if lnk != link and (lnk != None) and not (lnk in black_listed) and not ('#' in lnk) and not (lnk in landing_links) and not ('.jpg' in lnk) and not ('github' in lnk) and not ('/tools.' in lnk) and not ('/mcl/' in lnk) and not ('.ciscosystems.' in lnk) and not ('community.cisco'in lnk) and not ('/mibs' in lnk) and not ('Plug-and-Play' in lnk) and not('cfnng.cisco.com' in lnk):
                further_links.append(lnk)
    except:
        pass
        
    try:
        s1 = driver.find_element(By.TAG_NAME, "tr")
        switch_term = s1.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'step')]")
    except:
        switch_term = []
        
    if(switch_term):
        landing_page = True
    else:
        landing_page = False
    
    
    return landing_page, further_links


def get_landing_links(start_page_link):

    index_links = []
    hist = []
    landing_page_links = []
    index_links.append(start_page_link)

    while(True):

        new_links = []
        for link in index_links:
            landing_page, further_links = search_page(link, landing_page_links)
            
            if(landing_page):
                landing_page_links.append(link)
            else:
                for lk in further_links:
                    if lk in hist:
                        further_links.remove(lk)
                    else:
                        hist.append(lk)

                new_links += further_links

        index_links = new_links.copy()

        if(len(index_links) == 0):
            break

    return landing_page_links