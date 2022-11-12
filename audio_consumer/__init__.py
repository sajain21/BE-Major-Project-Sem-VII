
def init_consumer(consumer_name):

    from .connect import cur, conn

    from .consumer import run_mq

    run_mq(consumer_name)