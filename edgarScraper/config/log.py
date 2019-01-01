import logging
log = logging.getLogger("mylog")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
     "{asctime} {levelname} {message}", style='{'
     )

# Log to file
#filehandler = logging.FileHandler("debug.txt", "w")
#filehandler.setLevel(logging.DEBUG)
#filehandler.setFormatter(formatter)
#log.addHandler(filehandler)

# Log to stdout too
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)
streamhandler.setFormatter(formatter)
log.addHandler(streamhandler)