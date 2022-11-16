from multiprocessing import freeze_support, set_start_method, Process, pool, Pool
import time
import datetime
import os


def run_process(*args, **kwargs):
    message, callback = args[0], args[1]
    # if semaphore.acquire():
    data = message.value.decode()
    topic_name = message.topic
        # logging.debug("recv topic name {}, data: {}".format(topic_name, data))
        # print(("recv topic name {}, data: {}".format(topic_name, data, datetime.datetime.now())))
    print(("recv topic name {}, data: {}".format(topic_name, datetime.datetime.now())))
    callback(data, topic_name)
    print("________________test_______________")
    

def deal_process(consumer, callback):
      # 控制每次最多执行 5 个线程
    start_time = time.perf_counter()
    threads = []
    with pool.Pool(processes=3) as p:
        index =0
        for message in consumer:
        # run_thread_instance = threading.Thread(target=run_thread, args=( message, callback))
            param = [(message, callback)]
            index += 1
            data = p.apply_async(func=run_process,
                                 args=(message,callback), kwds={"key": "value"},
                                )
            print(data)
        # run_thread_instance.join()

        p.join()
    # theard_pool.shutdown(wait= True)
    print("累计耗时：", time.perf_counter() - start_time)

result_list = list()

def log_result(result):
    result_list.append(result)


def work(*args, **kwargs):
    t_start = time.time()

    print("%d号任务开始执行，进程号为%d" % (args[0], os.getpid()))

    print(kwargs)
    t_stop = time.time()
    print("%d号任务执行完毕，耗时%0.2f" % (args[0], t_stop - t_start))

    print()  # 换行使结果更清晰

    return args[0]