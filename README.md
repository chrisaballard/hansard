# Hansard Explorer
🏛️ Explore Parliamentary debates

[Hansard](https://hansard.parliament.uk/) is the official report of all Parliamentary debates.

This project processes the data from the My Society [parlparse](https://github.com/mysociety/parlparse) parser. This parser generates XML files in ParlParse format, containing debates, petititons and divisons.

This project uses this XML data as a source in order to:

- Convert it to json which is more practical to work with
- Detect key entities contained in debates such as organisations, committees and people
- Disambiguate entities - e.g. `HMRC` and `His Majesty's Revenue and Customs` refer to the same entity

## References
- [ParlParse parser](https://github.com/mysociety/parlparse)
- [ParlParse dataset format](https://parser.theyworkforyou.com/hansard.html)