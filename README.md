# Contact Translator
For the longest time my phone's system language has been in English but naturally I kept saving contacts in Hebrew as it is the language I speak every day.
However these languages conflict eachother due to their typing direction which makes for some visual incompatibilities and I had way too many contacts to manually translate each one, so I wrote a script to automate it.

Originally it made sense to just utilize Google's translation module to take an input .vcf file and spit out the translations, however I did not take into account that it would translate most names quite literally.
![image](https://github.com/user-attachments/assets/d7b14c2f-ffb1-45fe-8db1-1ffce5c8cc22)

Eventually I realized the optimal solution is to find a dictionary/translation website which is natively using the origin language for it to be able to translate names properly.
The names were extracted from the file and sent via a POST request to the website containing each name as a variable in the payload and reading the received output for the translations.

