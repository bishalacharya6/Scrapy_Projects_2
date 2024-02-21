# web scraping framework
import scrapy
# for regular expression
import re
# for selenium request
from scrapy_selenium import SeleniumRequest
# for link extraction
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class EmailSpider(scrapy.Spider):

    name = 'email'

    uniqueemail = set()

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.geeksforgeeks.org/",
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        # Extract the list of links in the site
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        FinalLinks = [str(link.url) for link in links]
        # print(f'This is the Final list of Links: {FinalLinks}')

        # Write the links to a text file
        with open('finallistlinks.txt', 'w', encoding='utf-8') as file:
            for f in FinalLinks:
                file.write(f + '\n')

        # Empty list
        links = []

        # Filtering the needed lists
        for link in FinalLinks:
            if ('Contact' in link or 'contact' in link or 'About' in link or 'about' in link or 'CONTACT' in link or 'ABOUT' in link):
                links.append(link)

        links.append(str(response.url))

        l = links[0]
        links.pop(0)

        # This meta helps to transfer the list of the links to the parse_links function successfully
        yield SeleniumRequest(
            url=l,
            wait_time=3,
            screenshot=True,
            callback=self.parse_link,
            dont_filter=True,
            meta={'links': links}
        )

    def parse_link(self, response):
        # This helps to get the links from the parse function
        links = response.meta['links']
        flag = 0

        # The links that contain the bad words are removed from the links list
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']

        # Raising the flag level to 1 when bad words are found
        for words in bad_words:
            if words in str(response.url):
                flag = 1
                break

        if flag != 1:
            # Corrected line to extract HTML content
            html_text = response.text

            email_list = re.findall('\w+@\w+\.{1}\w+', html_text)

            email_lists = set(email_list)
            if len(email_lists) != 0:
                for i in email_lists:
                    self.uniqueemail.add(i)

        if len(links) > 0:
            l = links[0]
            links.pop(0)

            yield SeleniumRequest(
                url=l,
                callback=self.parse_link,
                dont_filter=True,
                meta={"links": links}
            )
        else:
            yield SeleniumRequest(
                url=response.url,
                callback=self.parsed,
                dont_filter=True
            )

    def parsed(self, response):
        # Emails list of uniqueemail set
        emails = list(self.uniqueemail)
        finalemail = []

        for email in emails:
            # Avoid garbage value by using '.in' and '.com'
            # Append email ids to finalemail
            if ('.in' in email or '.com' in email or 'info' in email or 'org' in email):
                finalemail.append(email)

        # Final unique email ids from geeksforgeeks site
        print('\n'*2)
        print("Emails scraped", finalemail)
        print('\n'*2)
