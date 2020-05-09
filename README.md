# Edgar Debt Scraper

This is an application designed for large-scale 10Q debt term extraction from the EDGAR database.  

- after cloning the git repo, try 'python -m unittest' and verify  that all tests run successfully. 
- usage examples, implementation notes, and additional data analysis are provided in the notebook directory.
- Using this application I was able to process 561,794 10Qs from 1994 - 2019 with roughly 85% of 10Qs yielding short and longterm debt levels.

![title](notebooks/systemDiagram.jpg)

## Usage Example

The application's main entry point is a method of the EdgarDebtScraper class called runJob.    

<pre><code> from edgarScraper.edgarDebtScraper import EdgarDebtScraper
eds = EdgarDebtScraper()
? eds.runJob()


Signature: eds.runJob(outputFile=None, years=None, ciks=None, maxFiles=1000, nScraperProcesses=8, nIndexProcesses=8)
Docstring:
main entry method for scraping jobs.  Will write results to
the data directory in form <outputFile>_<year> and disclosures_year if
an outputFile is passed.  Otherwise, it will return a debtline item
dataframe and disclosures dataFrame if no outputFile is supplied.

Note:
    - if a list of specific ciks is supplied, maxFile limit is ignored,
    and the complete set of relevant urls will be eagerly built from
    a distributed search routing.  If no ciks are supplied it will
    lazily iterate through 10Q urls.
    - for large jobs supply an outputFile so that results can be
    periodically written to disk.  Otherwise, pandas dataFrames will
    be built in memory.

Args:
    outputFile: String name of file to write results to.
    years: list of years to restrict 10Q iteration to.
    ciks: list of ciks to restrict 10Q search to
    maxFiles: integer number of maximum files to iterate through
    nScraperProcesses: number of processes to use for processing 10Qs
    nIndexProcesses: number of processes to use for distributed cik
        search.

Returns:
    None if an outputFile is supplied.
    (dataFrame, dataFrame) if no outputFile is supplied 
</code></pre>

## Data Heirachy

The application attempts to find relevant debt-information for 71 different fields.  These fields and the accompanying taxonomy are taken from information found on https://xbrl.us/.  

Final short and long term debt levels are calculated based upon the following strategy:

  1) If values exist for key fields like ```LONGTERMDEBTNONCURRENT``` or ```DEBTCURRENT``` return these values as the final long and short-term debt levels.

  2) Else, attempt to form final results by aggregating up component subfields. 

  3) Finally, if the first two approaches fail, attempt to form results by taking values from parent-fields (usually total current / non current liabilities) and subtracting "sibling-level" fields where applicable.
    
For more details on this aggregation logic please see the source code contained in ```edgarScraper.pipelineIO.resultset.py```

As with other implementation decisions, there are pros and cons to the approach I took.  A pro is that the logic employed closely matches standard GAAP Taxonomies and allows for a robust and systematic way of determining overall debt levels.  Indeed, using this approach I was able to get viable values for close to 90% of all 10-Q filings from 1994-2018.  

**The disadvantage to this approach is that it can sometimes lead to apples-to-oranges type comparisons.  For instance, for a given 10-Q, the only short term debt field recovered may be a company's total current liabilities - either because the company provided little information or extraction faired poorly.  This value will likely overstate the company's short term debt (as it can include things like payroll and taxes).  For a different 10-Q, a more granular short-term debt field may be the only one resolved.  Under the scheme advanced, both values will appear as final short term debt levels.**  

### Data Field Groupings and Hierarchy
![title](notebooks/fields.jpg)
