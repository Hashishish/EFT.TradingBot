from loguru import logger


def foo():
    logger.info("Inside foo")


def bar():
    logger.info("Inside bar")


@logger.catch
def baz():
    a = 1 / 0


foo()
bar()
baz()
