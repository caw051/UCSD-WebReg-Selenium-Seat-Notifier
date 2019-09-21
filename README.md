
# WebReg-Selenium-Seat-Extractor
Designed as proof of concept and for showcasing selenium based skill, it logins into UCSD's WebReg and extracts a sample class(in this case, PHYS 2C B01) and gets the # of seats that are present for that particular section. Only applicable for UCSD based credentials.

This was originally transferred from another repo I worked on(previously with 23 commits), primarily to make it more viewable for public.

Many problems and lessons faced:

# 1. The Design Choice(BeautifulSoup ------> Selenium)

When doing the BeautifulSoup and urllib requests, I realized that Beautifulsoup was far too lightweight to let me deal with logging in with dynamic webpages like WebReg, since it would end up returning a empty content, despite successful login. After enough searching, I came to discover that any webpages that dynamically generate HTML content through the help of langauges like Javascript causes BeautifulSoup to prematurely get the HTML content when it did not load all of the HTML content yet. Thus, I resorted to using to Selenium in order to solve that problem.

Sometimes, it may be hard to realize that the tool you may use leads to a dead end until you actually attempt a complex project with it(like Webreg) and see its shortcomings(Selenium's slow speeds, BeautifulSoup's reliance on other libraries for complex web pages, etc)


# 2. Web scraping should never be used as a first resort.

In Selenium, the single most powerful tool to navigate and search for elements is through search via Xpath.

Xpath is to web scraping(and XML) as regex is to Vim. 

Xpath is extremely useful for doing things like going up one parent node, or being able to find tags with specific text or attribute(e.g. "contains <text>=text()" or "@aria-describedby") but it is something I would prefer to avoid using because of its hackiness and its tendency to be too brittle. 

Of course, I have attempted to mitigate those effects by carefully crafting the Xpath to make it more flexible to change(based on the tag's description), and to save as much navigating steps as I can, but any serious design changes to the website or the html generation process would still obsolete my code.

That is why using an API is far more preferrable for getting data. I initially started the project precisely because I discovered that no such API was found/available to use at the time.

If anything, it is much more effective as a backup in case the heavily-relied upon API is unavailable(or stops working and needs a temporary replacement).


# 3. Edge Cases

Various edge cases such as "style=display:none" are unextractable with .text(), as well as the fact that you cannot directly check for a completely blank text with &nbsp without resorting to tricks like <HTMLtag>.get_attribute("textContent") != '\xa0'. Many more exist, and you cannot really expect any website to work consistently, which leads to #4.


# 4. The Importance of Try-Catch Statements and Print Statements

Try and catch statements are very crucial to any kind of web scraping, but must be used with discretion since they do a good job hiding unintended exceptions or bugs; much of the print statements used for debugging were therefore placed in those try except statements and it saved me a considerable amount of time debugging and detecting the source of the exception(s) that occurs.
