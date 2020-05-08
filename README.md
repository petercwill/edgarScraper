to test installation try 'python -m unittest' all tests should run successfully.

to play around with the scraper please see the 'usage examples and implementation notes' in the notebooks directory

# Usage Examples and Implementation Notes

This Notebook is meant to demonstrate a few usage examples of the application I developed for edgar debt scraping, as well as, provide some details and context around implementation.

A high level system diagram of the application is shown below.  The system was designed so that individual files could be processed in streaming fashion, meaning that applicable 10Qs would be lazily located and processed into final results in iterative fashion.

![title](systemDiagram.jpg)
