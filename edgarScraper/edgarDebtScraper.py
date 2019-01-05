from edgarScraper.pipelineIO.fileHandler import FileHandler
from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator
from edgarScraper.pipelineIO.resultSet import ResultSet
from edgarScraper.config.log import edgarScraperLog
import pandas as pd
import multiprocessing
from edgarScraper.pipelineIO.utils import iteratorSlice


def _url2Result(urlResults, fh):
    count = 0
    for res in urlResults:
        count += 1
        lineItems = fh.extractDebt(res.url)
        if lineItems:
            rs = ResultSet(cik=res.cik, name=res.name, date=res.date)
            rs.processLineItems(lineItems)
            yield rs


def _processFilesToDisk(urlResults, fh, file):

    f = open(file, 'w')
    for (i, res) in enumerate(_url2Result(urlResults, fh)):

        f.write(str(res))
        if i % 100 == 0:
            edgarScraperLog.info("Scraped {} total files".format(i))

    f.close()
    edgarScraperLog.info("Job Finished {} total files".format(i))
    return f


def _processFilesToDF(urlResults, fh, file):

    dictList = []
    for (i, res) in enumerate(_url2Result(urlResults, fh)):
        dictList.append(res._toDict())

        if i % 100 == 0:
            edgarScraperLog.info("Scraped {} total files".format(i))

    df = pd.DataFrame.from_records(dictList)
    edgarScraperLog.info("Job Finished {} total files".format(i))

    return df


class EdgarDebtScraper(object):

    def __init__(self):
        self.fh = FileHandler()
        self.log = edgarScraperLog

    # single Process job
    def runJob(
        self,
        outputType,
        outputFile=None,
        years=None,
        ciks=None,
        maxFiles=1000
    ):

        urlResults = FileUrlGenerator(years, ciks, maxFiles).getUrlGenerator()

        if outputType == "file":
            if outputFile is None:
                raise ValueError(
                    "Must specifiy output file when writing to disk"
                )

            else:
                result = _processFilesToDisk(urlResults, self.fh, outputFile)
                return result

        if outputType == 'pandas':
            df = _processFilesToDF(urlResults, self.fh, outputFile)
            df.set_index(['cik', 'date'], inplace=True)
            return df

        return result

    def runJobDist(
        self,
        nProcesses,
        outputType,
        outputFile=None,
        years=None,
        ciks=None,
        maxFiles=10000
    ):

        resultFrames = []

        pool = multiprocessing.Pool(processes=nProcesses)
        fh = FileHandler()
        fGen = FileUrlGenerator(years, ciks, maxFiles).getUrlGenerator()
        fGenIterator = iteratorSlice(fGen, 2)

        queue = []

        if outputType == "file":
            if outputFile is None:
                raise ValueError(
                    "Must specifiy output file when writing to disk"
                )

            else:
                func = _processFilesToDisk

        if outputType == 'pandas':
            func = _processFilesToDF

        while fGenIterator or queue:
            try:
                queue.append(
                    pool.apply_async(
                        func, [next(fGenIterator), fh, outputFile]
                    )
                )

            except (StopIteration, TypeError):
                fGenIterator = None

            while queue and (
                len(queue) >= pool._processes or not fGenIterator
            ):
                process = queue.pop(0)
                process.wait(0.1)
                if not process.ready():
                    queue.append(process)
                else:
                    res = process.get()
                    if res:
                        resultFrames.append(res)
        pool.close()

        if outputType == 'pandas':

            df = pd.concat(resultFrames, axis=0)
            df.set_index(['cik', 'date'], inplace=True)
            return df

        if outputType == 'file':
            return resultFrames[0]
