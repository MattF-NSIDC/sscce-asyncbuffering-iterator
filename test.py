import asyncio
import collections

mini = 0
increment = 5
maxi = mini + increment
max_results = increment * 3
buffer_warning_level = increment // 2


class AsyncGetData:
    def __init__(self):
        self.buffer = collections.deque([])
        self.buffer_source_depleted = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        need_more_data = (len(self.buffer) <= buffer_warning_level
                          and not self.buffer_source_depleted)
        data_remain = self.buffer or not self.buffer_source_depleted

        if not data_remain:
            raise StopAsyncIteration
        
        if need_more_data: 
            await self._prefetch()

        return await self._clean_data(self.buffer.popleft())

    async def _clean_data(self, data):
        """Control how quickly iterations can occur"""
        iteration_delay = 0.1  # in seconds
        await asyncio.sleep(iteration_delay)

        return data

    async def _prefetch(self):
        """Fake getting data from a server"""
        global mini
        global maxi

        server_delay = 1  # in seconds

        msg = "Buffer looks low ({}). Getting data (takes {} seconds)..."
        msg = msg.format(self.buffer, server_delay)
        print(msg)
        await asyncio.sleep(server_delay)

        if maxi <= max_results:
            page = list(range(mini, maxi))
        else:
            page = []
            print("No more pages of results available.")

        self.buffer.extend(page)
        print("Received {}, added to buffer: {}".format(page, self.buffer))

        mini = maxi
        maxi = maxi + increment

        if page == []:
            self.buffer_source_depleted = True


async def get_all_data():
    get_data = AsyncGetData()
    async for d in get_data:
        print("  Got data: {}".format(d))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_all_data())
    loop.close()
