import time
import asyncio
import logging
import datetime
import threading

async def deal_data(message, callback):
    # async with semaphore:
        data = message.value.decode()
        topic_name = message.topic
        # logging.debug("recv topic name {}, data: {}".format(topic_name, data))
        # print(("recv topic name {}, data: {}".format(topic_name, data, datetime.datetime.now())))
        print(("recv topic name {}, time: {}".format(topic_name, datetime.datetime.now())))
        callback(data, topic_name)

# async def run_task(consumer, callback):
#     semaphore = asyncio.Semaphore(51)
#     task_list = []
#     index = 0
#     msg_list = []
#     loop = asyncio.get_event_loop()
#     for message in consumer:
#         msg_list.append(message)
#         index += 1
#         print(index)
#         if index >19 :
#             loop.run_until_complete(asyncio.wait([get_title(semaphore, message, callback) for message in msg_list]))
#             msg_list = []
#             index = 0

    # tasks = [asyncio.ensure_future(get_title(semaphore, message, callback)) for message in consumer]
    # dones, pendings = await asyncio.wait(tasks)
    # print("------------start____________")
    # for task in dones:
    #     print(len(task.result()))


async def run_task(consumer, callback):
    semaphore = asyncio.Semaphore(20)
    task_list = []
    index = 0
    for message in consumer:
        # asyncio.create_task()
        one = asyncio.ensure_future(deal_data(semaphore, message, callback))
        task_list.append(one)
        index +=1
        # await asyncio.wait(task_list)
        start_time = time.perf_counter()
        one.result()
        print("代码运行时间为：", time.perf_counter() - start_time)
        # if index >19 :
        #     # semaphore = asyncio.Semaphore(10)
        #     await asyncio.gather(task_list)
        #     task_list = []
        #     index=0
        #     continue

async def main_run_task(consumer, callback):
    for message in consumer:
        print(f"started at {time.strftime('%X')}")
        task1 = asyncio.create_task(deal_data(message, callback))
        # await task1
        print(f"finished at {time.strftime('%X')}")
    await task1

if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(run_task())
    print("代码运行时间为：", time.perf_counter() - start_time)
    # 代码运行时间为： 2.227831242