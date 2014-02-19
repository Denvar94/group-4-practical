# Project Goal

To fill in

# Getting Started

This repositary only contains the source files. Everyone will need to download the data and generate the fake data for themselves. 

> git clone zzzz
> python setup.py


# Implementation

There are three distinct parts to the project. Each can be tackled seperately but it is expected that the parser will take up a disproporiate amount of time.

## Parser

The data is initially downloaded using the requests library and then stored in bin/raw/. Setup.py will download this for you if it doesn't exist.

Beautiful Soup is a Python library which makes light work of parsing HTML documents into usable formats. Once the information is downloaded, most of the work will be working out how we can coerce this tree into the infromation we want.

Once we have parsed the data, we can dump the information into some sort of database. Probably either sqlite3 of mongodb.

## API

This step will link together the database and the visualisation. How this is implemented depends a lot on how we decide to do the visualisation.

## Visualisation

It was suggested that we did this in the browser, I think this is a good idea. There are lots of javascript libraries which will allow for as much or as little control we like over the visualisation.

One suggestion was using D3 (http://d3js.org/), not something I have ever done.

There are about a million different ways though (http://www.creativebloq.com/design-tools/data-visualization-712402)
