from edgarScraper.pipelineIO.fileParser import FileParser
from edgarScraper.config.log import edgarScraperLog
import pandas as pd
import multiprocessing
from edgarScraper.pipelineIO.utils import iteratorSlice
from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator
import os
from collections import deque
from edgarScraper.config.constants import DATA_DIR


def _mpJob(urlGen, file):
    '''
    Multiprocessing task must be defined at top-level.  Each worker process
    iterates over a slice of the url-generator.  Urls are processed and
    results are returned to the main processes for aggregation.
    '''
    parser = FileParser()
    resDictList = []
    ddList = []

    for url in urlGen:

        (res, dd) = parser.fileUrl2Result(url)
        resDictList.append(res._toDict())
        ddList.append(dd._asdict())

    if url.seqNo % 100 == 0:
        edgarScraperLog.info('finished consuming file {}'.format(url.seqNo))

    return (resDictList, ddList)


class EdgarDebtScraper(object):
    """ Main Application

        Suppors iteration through 10Qs and extraction of debt-levels and
        disclosure text blocks for both single process and multiprocess jobs.

        Args:
            sliceSize (int): size of urlGenerator slice given to workers in
                distributed jobs.

        """

    def __init__(self, sliceSize=10):
        self.sliceSize = 10
        self.lineItemBuffer = []
        self.disclosureBuffer = []

    def _writeResultsToFile(self, df, filename):

        years = list(set(df['DATE'].dt.year.values))
        yearTuples = [(year, df[df['DATE'].dt.year == year]) for year in years]

        for year, chunk in yearTuples:
            fullFileName = filename+"_{}.csv".format(str(year))
            fout = os.path.join(DATA_DIR, fullFileName)
            edgarScraperLog.info(
                'dumping {} records to file {}'.format(chunk.shape[0], fout)
            )
            fh = open(fout, 'a')
            chunk.to_csv(fout, mode='a', header=fh.tell() == 0)
            fh.close()

    def _recordResults(self, lineItems, disclosures, outputFile):
        '''
        take a partial list of results and write to disk or store in buffer
        '''

        lineItemsDf = pd.DataFrame.from_records(lineItems)
        lineItemsDf['DATE'] = pd.to_datetime(lineItemsDf['DATE'].astype(str))

        disclosuresDf = pd.DataFrame.from_records(disclosures)
        disclosuresDf['DATE'] = pd.to_datetime(
            disclosuresDf['DATE'].astype(str)
        )

        if outputFile:
            self._writeResultsToFile(lineItemsDf, outputFile)
            self._writeResultsToFile(disclosuresDf, outputFile+'_disclosures')

        else:
            self.lineItemBuffer.append(lineItemsDf)
            self.disclosureBuffer.append(disclosuresDf)

    def _runSingleProcess(self, urlGen, outputFile):
        '''
        Single process implementation.  Iterates through urls in the generator
        and builds result dataframe in memory.  Suitable for smaller data
        pulls.
        '''

        parser = FileParser()
        lineItems = []
        disclosures = []
        for (i, url) in enumerate(urlGen, 1):
            res, dd = parser.fileUrl2Result(url)
            lineItems.append(res._toDict())
            disclosures.append(dd._asdict())

            if (i % 25 == 0):
                edgarScraperLog.info("Scraped {} total files".format(i))

            if (i % 100 == 0):
                self._recordResults(lineItems, disclosures, outputFile)
                lineItems = []
                disclosures = []

        edgarScraperLog.info("Job Finished {} total files".format(i))

        if lineItems:
            self._recordResults(lineItems, disclosures, outputFile)

        if not outputFile:
            lineItemDf = pd.concat(self.lineItemBuffer)
            disclosureDf = pd.concat(self.disclosureBuffer)
            return (lineItemDf, disclosureDf)

    def _runMultiProcess(
        self,
        urlGen,
        outputFile,
        maxFiles,
        nProcesses
    ):

        '''
        Multiprocess implementation.  Fileurl Generator is lazily read from
        inorder to fill a queue.  Workers takes a slice of urls from the queue
        and begin scraping debt information from the files.  The main processes
        periodicially checks the queue for finished workers and aggregates
        their results.  Results are written to disk every 1000 10-Qs.
        '''

        lineItems = []
        disclosures = []
        urlGenIter = iteratorSlice(urlGen, self.sliceSize)
        pool = multiprocessing.Pool(processes=nProcesses)
        queue = deque()

        while (urlGenIter or queue):
            try:
                queue.append(
                    pool.apply_async(
                        _mpJob, [next(urlGenIter), outputFile]
                    )
                )

            except (StopIteration, TypeError):
                urlGenIter = None

            while (
                queue and
                ((len(queue) >= 2*pool._processes) or not urlGenIter)
            ):
                process = queue.popleft()
                process.wait(.1)
                if not process.ready():
                    queue.append(process)
                else:
                    lineItemChunk, disclosureChunk = process.get()
                    lineItems.extend(lineItemChunk)
                    disclosures.extend(disclosureChunk)

                    if len(lineItems) >= 100:
                        self._recordResults(lineItems, disclosures, outputFile)
                        lineItems = []
                        disclosures = []

        pool.close()

        if lineItems:
            self._recordResults(lineItems, disclosures, outputFile)

        edgarScraperLog.info("Job Finished")

        if not outputFile:
            lineItemDf = pd.concat(self.lineItemBuffer)
            disclosureDf = pd.concat(self.disclosureBuffer)
            return (lineItemDf, disclosureDf)

    def runJob(
        self,
        outputFile=None,
        years=None,
        ciks=None,
        maxFiles=1000,
        nScraperProcesses=8,
        nIndexProcesses=8
    ):

        """main entry method for scraping jobs.  Will write results to
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

        """

        urlGen = FileUrlGenerator(
            years,
            ciks,
            maxFiles,
            nIndexProcesses
        ).getUrlGenerator()

        if nScraperProcesses == 1:
            result = self._runSingleProcess(
                urlGen,
                outputFile,
            )

        if nScraperProcesses > 1:
            result = self._runMultiProcess(
                urlGen,
                outputFile,
                maxFiles,
                nScraperProcesses
            )

        return(result)
