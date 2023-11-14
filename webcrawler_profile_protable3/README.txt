# Program Name webcrawler_profile_portable
- Name, Title, About, Experience, Education and	Skills are scraped from the LinkedIn profile
	
## General Information
- If the same LinkedIn account is used, it is recommended to run this program with a number of around 100 profiles a day or about 10-12 companies.(Preferrably less, as my accounts were still getting blocked)
  Any more and there is a larger chance that the LinkedIn account might be blocked for a few hours as the first warning. For the second warning the account will be blocked for about a day. After that it will be blocked permanently as it will now require you to identify yourself with an ID or phone numebr.
- Do not change the names of any of the files 

## Requirements

- Installed the latest Google Chrome web browser (I don't know if it works if you do not have a chrome web browser installed)
- LinkedIn account (use a fake one, and try to create multiple accounts)
- Some LinkedIn profile URLs (This you will need to manually search for,

## Instructions
1. In the **credentials.txt** file enter the username and password of the linkedin account. The username and password are separated by a colon. Example: usernameEmail:password
2. In the same folder, find the **data.txt** file. This file is used to specify the companies and LinkedIn URLs to be crawled. Follow the structure outlined below:
   
   - Start with a number on the first line, which represents the company index you are looking at.
   - Below the company index line, list the LinkedIn URLs of individuals working at that company, with each URL on a separate line.
   - If you have additional companies, add another number (company index) after the last LinkedIn URL and list the corresponding LinkedIn URLs for the new company.
   - The order of company indexes does not need to be sequential or in any particular order.
   - Do not leave line gaps and start from the first line in the text file.
   
Structure:
   
1
LinkedIn URL of person working at company 1
LinkedIn URL of person working at company 1
LinkedIn URL of person working at company 1
99
LinkedIn URL of person working at company 99
25
LinkedIn URL of person working at company 25
LinkeIn URL of person working at company 25
LinkedIn URL of person working at company 25

An Example:
1
https://www.linkedin.com/in/dirk-mcmahon-ba8375a7/
https://www.linkedin.com/in/sandeepdadlani/
2
https://www.linkedin.com/in/jenhsunhuang/

   
   Save the file once you have entered the required information.

3. Run the program, This will open a console window and a Chrome window.

4. For the first run or when running the program again after a few weeks, follow these additional steps:
   
   - On the Chrome window's login page, wait for the program to automatically enter the account details (approximately 20 seconds).
   - On the next page, you may encounter a prompt asking for phone number verification. If prompted, click "Skip."
   - You can then minimize the Chrome window, and the program will continue running normally until completion.
   - If you do not see a prompt to verify the phone number, you can skip this step.

5. Do not close the console window or the Chrome window until the program has finished running.

6. The program will continue running until completion. You can identify that the program has finished when the Chrome window closes or when you see the "finished" message in the console window. At this point, you can close the console window.

7. The program's output will be located in the **LinkedIn_Data** folder.

8. If you need to stop the program from running, you can simply close the console window at any point.
   
   - To resume the program after an interruption, check the **LinkedIn_Data** folder to determine which companies have been completed and which company was interrupted. The interrupted company will be the one that was modified most recently.
   - In the **data.txt** file, remove all the completed companies and their respective LinkedIn URLs, except for the interrupted company and its URLs and any not completed companies. Save the changes to the file and start the program again.

