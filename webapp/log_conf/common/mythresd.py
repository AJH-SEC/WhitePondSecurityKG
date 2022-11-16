import threading
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio

theard_pool = ThreadPoolExecutor(max_workers=20)

# semaphore = threading.Semaphore(100)
async def run_thread(message, callback):
    # if semaphore.acquire():
        data = message.value.decode()
        topic_name = message.topic
        # logging.debug("recv topic name {}, data: {}".format(topic_name, data))
        # print(("recv topic name {}, data: {}".format(topic_name, data, datetime.datetime.now())))
        print(("recv topic name {}, data: {}".format(topic_name, datetime.datetime.now())))
        # callback(data, topic_name)
        print("________________test_______________")
        return "test"
    

def deal_thread(consumer, callback):
      # 控制每次最多执行 5 个线程
    start_time = time.perf_counter()
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for message in consumer:
            print("---da")
            # run_thread_instance = threading.Thread(target=run_thread, args=( message, callback))
            executor.submit(run_thread, message, callback)
            # run_thread_instance.join()
    # theard_pool.shutdown(wait= True)
    print("累计耗时：", time.perf_counter() - start_time)

def deal_thread_async(consumer, callback):
    calculator = FibonacciCalculatorAsync()
    calculator.start_loop()
    for message in consumer:
        calculator.run(message, callback)


class FibonacciCalculatorAsync:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # self.loop = asyncio.get_event_loop()

    @staticmethod
    def calculate_sync(message, callback):
        return run_thread(message, callback)

    async def calculate(self, message, callback):
        # result = await self.loop.run_in_executor(self.loop, run_thread, message, callback)
        await run_thread(message, callback)
        print("finsta")

    def run(self, message, callback):
        asyncio.run_coroutine_threadsafe(self.calculate(message, callback), self.loop)

    def start_loop(self):
        thr = threading.Thread(target=self.loop.run_forever)
        thr.daemon = True
        thr.start()


def deal_thread(message, callback):
    # if semaphore.acquire():
        data = message.value.decode()
        topic_name = message.topic
        # logging.debug("recv topic name {}, data: {}".format(topic_name, data))
        # print(("recv topic name {}, data: {}".format(topic_name, data, datetime.datetime.now())))
        print(("recv topic name {}, data: {}".format(topic_name, datetime.datetime.now())))
        callback(data, topic_name)
        print("________________test_______________")
        return 

def start_thread_fuc(consumer, callback):
    for message in consumer:
        length = len(threading.enumerate())
        print('当前运行的线程数为：%d' % length)
        thread_one = threading.Thread(target=deal_thread, args=(message, callback))
        # deal_thread(message, callback)
        theard_pool.shutdown
        thread_one.start()


def start_thread_pool(consumer, callback):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for message in consumer:
            # 提交任务
            length = len(threading.enumerate())
            print('当前运行的线程数为：%d' % length)
            executor.submit(run_thread_pool, message, callback)

def run_thread_pool(message, callback):
    data = message.value.decode()
    topic_name = message.topic
    print(("recv topic name {}, data: {}".format(topic_name, datetime.datetime.now())))
    callback(data, topic_name)
    print("________________test_______________")

