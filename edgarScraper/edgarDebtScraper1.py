from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.config.log import edgarScraperLog
import pandas as pd
import multiprocessing
from edgarScraper.pipelineIO.utils import iteratorSlice
from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator
import os

# distributed function - must be pickle-able, define at top-level
# def _mpToFile(urlGen, file):

#     processor = ResultGenerator()
#     with open(file, 'a') as f:
#         for (i, url) in enumerate(urlGen):
#             res = processor.fileUrl2Result(url)
#             f.write(str(res))
#     return (i, None)


def _mpToDf(urlGen, file):

    processor = ResultGenerator()
    dictList = []
    for (i, url) in enumerate(urlGen):
        res = processor.fileUrl2Result(url)
        if url.seqNo % 100 == 0:
            edgarScraperLog.info('consuming file {}'.format(url.seqNo))
        dictList.append(res._toDict())
    #dictList = [processor.fileUrl2Result(url)._toDict() for url in urlGen]
    df = pd.DataFrame.from_records(dictList)
    return (len(dictList), df)


class EdgarDebtScraper(object):

    def __init__(self):
        pass

    def _spToFile(self, urlGen, file, maxFiles):

        f = open(file, 'w')
        processor = ResultGenerator()
        for (i, url) in enumerate(urlGen):
            res = processor.fileUrl2Result(url)
            f.write(str(res))

            if i % 25 == 0:
                edgarScraperLog.info("Scraped {} total files".format(i))

            if (i >= maxFiles):
                break

        f.close()
        edgarScraperLog.info("Job Finished {} total files".format(i))
        return f

    def _spToDf(self, urlGen, maxFiles):
        dictList = []
        processor = ResultGenerator()
        for (i, url) in enumerate(urlGen):
            res = processor.fileUrl2Result(url)
            dictList.append(res._toDict())

            if i % 25 == 0:
                edgarScraperLog.info("Scraped {} total files".format(i))

            if (i >= maxFiles):
                break

        df = pd.DataFrame.from_records(dictList)
        df.set_index(['CIK', 'DATE'], inplace=True)
        edgarScraperLog.info("Job Finished {} total files".format(i))

        return df

    def _runSingleProcess(self, urlGen, outputType, outputFile, maxFiles):

        if outputType == "file":
            result = self._spToFile(urlGen, outputFile, maxFiles)

        if outputType == "pandas":
            result = self._spToDf(urlGen, maxFiles)

        return result

    def _runMultiProcess(
        self,
        urlGen,
        outputType,
        outputFile,
        maxFiles,
        nProcesses
    ):
        urlGenIter = iteratorSlice(urlGen, 10)
        pool = multiprocessing.Pool(processes=nProcesses)
        #results = []

        if outputType == "file":
            f = _mpToFile

        if outputType == "pandas":
            f = _mpToDf

        queue = []

        while (urlGenIter or queue):
            try:
                queue.append(
                    pool.apply_async(
                        f, [next(urlGenIter), outputFile]
                    )
                )

            except (StopIteration, TypeError):
                urlGenIter = None

            while (
                queue and
                (len(queue) >= pool._processes or not urlGenIter)
            ):
                process = queue.pop(0)
                # process.wait(1)
                if not process.ready():
                    queue.append(process)
                else:
                    i, df = process.get()
                    df.set_index(['CIK', 'DATE'], inplace=True)

                    fout = open(outputFile, 'a')
                    df.to_csv(fout, mode='a', header=fout.tell() == 0)
                    fout.close()

                    # results.append(result)
        pool.close()

        # if outputType == "file":
        #     return

        # if outputType == "pandas":
        #     df = pd.concat(results, axis=0)
        #     df.set_index(['CIK', 'DATE'], inplace=True)
        #     return df

    def runJob(
        self,
        outputType,
        outputFile=None,
        years=None,
        ciks=None,
        maxFiles=1000,
        nScraperProcesses=8,
        nIndexProcesses=8
    ):

        urlGen = FileUrlGenerator(years, ciks, maxFiles, nIndexProcesses).getUrlGenerator()

        if (outputType == 'file') and (outputFile is None):
            raise ValueError(
                "Must specifiy output file when writing to disk"
            )

        if nScraperProcesses == 1:
            result = self._runSingleProcess(
                urlGen,
                outputType,
                outputFile,
                maxFiles
            )

        if nScraperProcesses > 1:
            result = self._runMultiProcess(
                urlGen,
                outputType,
                outputFile,
                maxFiles,
                nScraperProcesses
            )

        return(result)





