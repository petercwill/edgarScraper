from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.config.log import edgarScraperLog
import pandas as pd
import multiprocessing
from edgarScraper.pipelineIO.utils import iteratorSlice
from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator
import os
from edgarScraper.pipelineIO.resultSet import DebtDisclosure
from collections import deque

DATA_DIR = os.path.realpath(
    os.path.join(os.path.realpath(__file__), '../../data/')
)


def _mpJob(urlGen, file):
    processor = ResultGenerator()
    resDictList = []
    ddList = []

    for url in urlGen:

        if url.seqNo < 43000:
            return None, None

        (res, dd) = processor.fileUrl2Result(url)
        resDictList.append(res._toDict())
        ddList.append(dd)

    if url.seqNo % 100 == 0:
        edgarScraperLog.info('finished consuming file {}'.format(url.seqNo))

    resDf = pd.DataFrame.from_records(resDictList)
    ddDf = pd.DataFrame.from_records(ddList, columns=DebtDisclosure._fields)

    return (resDf, ddDf)


class EdgarDebtScraper(object):

    def __init__(self):
        pass

    def writeResultsToFile(self, results, filename):
        df = pd.concat(results)

        df['DATE'] = pd.to_datetime(df['DATE'].astype(str))
        years = list(set(df['DATE'].dt.year.values))
        yearTuples = [(year, df[df['DATE'].dt.year == year]) for year in years]

        for year, chunk in yearTuples:
            fullFileName = filename+"_{}.csv".format(year)
            fout = os.path.join(DATA_DIR, fullFileName)
            edgarScraperLog.info(
                'dumping {} records to file {}'.format(chunk.shape[0], fout)
            )
            fh = open(fout, 'a')
            chunk.to_csv(fout, mode='a', header=fh.tell() == 0)
            fh.close()

    def _runSingleProcess(self, urlGen, maxFiles):
        dictList = []
        processor = ResultGenerator()
        print('hello')
        print(urlGen)

        import time
        start_time = time.time()
        for (i, url) in enumerate(urlGen):
            print(url)
            res, dd = processor.fileUrl2Result(url)
            end_time = time.time()
            elapse = end_time - start_time
            start_time = end_time
            print("Method: {}, Time {}".format(res.EXTRACTCODE, elapse))
            dictList.append(res._toDict())

            if i % 1 == 0:
                edgarScraperLog.info("Scraped {} total files".format(i))

            if (i >= maxFiles):
                break

        df = pd.DataFrame.from_records(dictList)
        df.set_index(['CIK', 'DATE'], inplace=True)
        edgarScraperLog.info("Job Finished {} total files".format(i))

        return df

    def _runMultiProcess(
        self,
        urlGen,
        outputFile,
        maxFiles,
        nProcesses
    ):

        sliceSize = 10
        lineItems = []
        disclosures = []
        urlGenIter = iteratorSlice(urlGen, sliceSize)
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

                    if not (lineItemChunk is None):

                        lineItems.append(lineItemChunk)
                        disclosures.append(disclosureChunk)

                        if len(lineItems) >= int(1000 / sliceSize):

                            self.writeResultsToFile(lineItems, outputFile)
                            self.writeResultsToFile(disclosures, 'disclosures')

                            lineItems = []
                            disclosures = []

        pool.close()

    def runJob(
        self,
        outputFile,
        years=None,
        ciks=None,
        maxFiles=1000,
        nScraperProcesses=8,
        nIndexProcesses=8
    ):

        urlGen = FileUrlGenerator(
            years,
            ciks,
            maxFiles,
            nIndexProcesses
        ).getUrlGenerator()

        if nScraperProcesses == 1:
            result = self._runSingleProcess(
                urlGen,
                maxFiles
            )

        if nScraperProcesses > 1:
            result = self._runMultiProcess(
                urlGen,
                outputFile,
                maxFiles,
                nScraperProcesses
            )

        return(result)
